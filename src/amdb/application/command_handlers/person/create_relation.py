from datetime import datetime, timezone

from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_relation import CreateRelation
from amdb.application.commands.person.create_relation import CreateRelationCommand
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.relation import RelationGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_RELATION_INVALID_COMMAND,
    CREATE_RELATION_ACCESS_DENIED,
    RELATION_ALREADY_EXISTS,
    PERSON_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class CreateRelationHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        create_relation: CreateRelation,
        access_policy_gateway: AccessPolicyGateway,
        relation_gateway: RelationGateway,
        person_gateway: PersonGateway,
        marriage_gateway: MarriageGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._create_relation = create_relation
        self._access_policy_gateway = access_policy_gateway
        self._relation_gateway = relation_gateway
        self._person_gateway = person_gateway
        self._marriage_gateway = marriage_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: CreateRelationCommand) -> None:
        required_access_policy = self._access_policy_gateway.for_create_relation()
        current_access_policy = self._identity_provider.get_access_policy()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(CREATE_RELATION_ACCESS_DENIED)

        relation = self._relation_gateway.with_person_id_and_relative_id(
            person_id=command.person_id,
            relative_id=command.relative_id,
        )
        if relation is not None:
            raise ApplicationError(RELATION_ALREADY_EXISTS)

        person = self._person_gateway.with_id(
            person_id=command.person_id,
        )
        if person is None:
            raise ApplicationError(
                message=PERSON_DOES_NOT_EXIST,
                extra={"person_id": command.person_id},
            )

        relative = self._person_gateway.with_id(
            person_id=command.relative_id,
        )
        if relative is None:
            raise ApplicationError(
                message=PERSON_DOES_NOT_EXIST,
                extra={"person_id": command.relative_id},
            )

        if person.sex is Sex.MALE and relative.sex is Sex.FEMALE:
            husband_marriages = self._marriage_gateway.list_with_husband_id(
                husband_id=person.id,
            )
            for husband_marriage in husband_marriages:
                if husband_marriage.wife_id != relative.id:
                    continue
                raise ApplicationError(
                    message=CREATE_RELATION_INVALID_COMMAND,
                    extra={"details": "Person is a relative's husband"},
                )
        elif person.sex is Sex.FEMALE and relative.sex is Sex.MALE:
            wife_marriages = self._marriage_gateway.list_with_wife_id(
                wife_id=person.id,
            )
            for wife_marriage in wife_marriages:
                if wife_marriage.husband_id != relative.id:
                    continue
                raise ApplicationError(
                    message=CREATE_RELATION_INVALID_COMMAND,
                    extra={"details": "Person is a relative's wife"},
                )

        relation = self._create_relation(
            person=person,
            relative=relative,
            type=command.type,
            timestamp=datetime.now(timezone.utc),
        )
        self._relation_gateway.save(
            relation=relation,
        )
        self._person_gateway.update(
            person,
            relative,
        )

        self._unit_of_work.commit()
