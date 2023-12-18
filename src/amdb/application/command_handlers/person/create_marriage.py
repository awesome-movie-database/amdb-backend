from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import MarriageId, MarriageStatus
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.application.commands.person.create_marriage import CreateMarriageCommand
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_PERSON_INVALID_COMMAND,
    CREATE_MARRIAGE_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
    PERSON_ALREADY_MARRIED,
    PERSONS_ALREADY_MARRIED,
    PERSONS_HAVE_SAME_SEX,
)
from amdb.application.common.exception import ApplicationError


class CreateMarriageHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        create_marriage: CreateMarriage,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._create_marriage = create_marriage
        self._access_policy_gateway = access_policy_gateway
        self._marriage_gateway = marriage_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: CreateMarriageCommand) -> MarriageId:
        required_access_policy = self._access_policy_gateway.for_create_marriage()
        current_access_policy = self._identity_provider.get_access_policy()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(CREATE_MARRIAGE_ACCESS_DENIED)

        husband, wife = self._ensure_husband_and_wife(
            husband_id=command.husband_id,
            wife_id=command.wife_id,
        )
        self._ensure_can_create_marriage(
            husband=husband,
            wife=wife,
            status=command.status,
        )
        children = self._ensure_children(
            father=husband,
            mother=wife,
            child_ids=command.child_ids,
        )

        marriage = self._create_marriage(
            id=MarriageId(uuid4()),
            husband=husband,
            wife=wife,
            children=children,
            status=command.status,
            timestamp=datetime.now(timezone.utc),
            start_date=command.start_date,
            end_date=command.end_date,
        )
        self._marriage_gateway.save(
            marriage=marriage,
        )
        self._person_gateway.update(
            person=husband,
        )
        self._person_gateway.update(
            person=wife,
        )
        self._person_gateway.update_list(
            persons=children,
        )

        self._unit_of_work.commit()

        return marriage.id

    def _ensure_husband_and_wife(
        self,
        *,
        husband_id: PersonId,
        wife_id: PersonId,
    ) -> tuple[Person, Person]:
        husband = self._person_gateway.with_id(
            person_id=husband_id,
        )
        if husband is None:
            raise ApplicationError(
                messsage=PERSON_DOES_NOT_EXIST,
                extra={"person_id": husband_id},
            )

        wife = self._person_gateway.with_id(
            person_id=wife_id,
        )
        if wife is None:
            raise ApplicationError(
                messsage=PERSON_DOES_NOT_EXIST,
                extra={"person_id": wife_id},
            )

        if husband.sex == wife.sex:
            raise ApplicationError(PERSONS_HAVE_SAME_SEX)

        return (husband, wife)

    def _ensure_can_create_marriage(
        self,
        *,
        husband: Person,
        wife: Person,
        status: MarriageStatus,
    ) -> None:
        valid_marriage_statuses = (
            MarriageStatus.DIVORCE,
            MarriageStatus.HIS_DEATH,
            MarriageStatus.HER_DEATH,
        )

        husband_marriages = self._marriage_gateway.list_with_husband_id(
            husband_id=husband.id,
        )
        for husband_marriage in husband_marriages:
            if (
                status is MarriageStatus.MARRIAGE
                and husband_marriage.status not in valid_marriage_statuses
            ):
                if husband_marriage.wife_id == wife.id:
                    raise ApplicationError(PERSONS_ALREADY_MARRIED)

                raise ApplicationError(
                    messsage=PERSON_ALREADY_MARRIED,
                    extra={"person_id": husband.id},
                )

        wife_marriages = self._marriage_gateway.list_with_wife_id(
            wife_id=wife.id,
        )
        for wife_marriage in wife_marriages:
            if (
                status is MarriageStatus.MARRIAGE
                and wife_marriage.status not in valid_marriage_statuses
            ):
                raise ApplicationError(
                    messsage=PERSON_ALREADY_MARRIED,
                    extra={"person_id": wife.id},
                )

    def _ensure_children(
        self,
        *,
        father: Person,
        mother: Person,
        child_ids: list[PersonId],
    ) -> list[Person]:
        if father.id in child_ids or mother.id in child_ids:
            raise ApplicationError(
                messsage=CREATE_PERSON_INVALID_COMMAND,
                extra={"extra_message": "Husband id or wife id in child ids"},
            )

        children = self._person_gateway.list_with_ids(
            *child_ids,
        )
        if len(children) != len(child_ids):
            child_ids_from_gateway = [child.id for child in children]

            invalid_child_ids = []
            for child_id in child_ids:
                if child_id in child_ids_from_gateway:
                    continue
                invalid_child_ids.append(child_id)

            raise ApplicationError(
                messsage=PERSONS_DO_NOT_EXIST,
                extra={"person_ids": invalid_child_ids},
            )

        return children
