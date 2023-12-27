from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.person.person import Person
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
    CREATE_MARRIAGE_INVALID_COMMAND,
    CREATE_MARRIAGE_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
    PERSON_IS_MARRIED,
    MARRIAGE_ALREADY_EXISTS,
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

        self._ensure_valid_command(
            command=command,
        )

        husband = self._person_gateway.with_id(
            person_id=command.husband_id,
        )
        if husband is None:
            raise ApplicationError(
                message=PERSON_DOES_NOT_EXIST,
                extra={"person_id": command.husband_id},
            )

        wife = self._person_gateway.with_id(
            person_id=command.wife_id,
        )
        if wife is None:
            raise ApplicationError(
                message=PERSON_DOES_NOT_EXIST,
                extra={"person_id": command.wife_id},
            )

        self._ensure_can_create_marriage(
            husband=husband,
            wife=wife,
            status=command.status,
        )

        children, missing_child_ids = self._person_gateway.list_with_ids(
            *command.child_ids,
        )
        if missing_child_ids:
            raise ApplicationError(
                message=PERSONS_DO_NOT_EXIST,
                extra={"person_ids": missing_child_ids},
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

    def _ensure_valid_command(
        self,
        *,
        command: CreateMarriageCommand,
    ) -> None:
        if command.husband_id in command.child_ids or command.wife_id in command.child_ids:
            raise ApplicationError(
                message=CREATE_MARRIAGE_INVALID_COMMAND,
                extra={"details": "Child ids contain id of husband or wife"},
            )

    def _ensure_can_create_marriage(
        self,
        *,
        husband: Person,
        wife: Person,
        status: MarriageStatus,
    ) -> None:
        valid_marriage_statuses_for_new_marriage_to_have = (
            MarriageStatus.MARRIAGE,
            MarriageStatus.HE_FILED_FOR_DIVORCE,
            MarriageStatus.SHE_FILED_FOR_DIVORCE,
        )
        valid_marriage_statuses_for_spouses_to_have = (
            MarriageStatus.DIVORCE,
            MarriageStatus.HIS_DEATH,
            MarriageStatus.HER_DEATH,
        )

        husband_marriages = self._marriage_gateway.list_with_husband_id(
            husband_id=husband.id,
        )
        for husband_marriage in husband_marriages:
            if (
                status in valid_marriage_statuses_for_new_marriage_to_have
                and husband_marriage.status not in valid_marriage_statuses_for_spouses_to_have
            ):
                if husband_marriage.wife_id == wife.id:
                    raise ApplicationError(MARRIAGE_ALREADY_EXISTS)

                raise ApplicationError(
                    message=PERSON_IS_MARRIED,
                    extra={"person_id": husband.id},
                )

        wife_marriages = self._marriage_gateway.list_with_wife_id(
            wife_id=wife.id,
        )
        for wife_marriage in wife_marriages:
            if (
                status in valid_marriage_statuses_for_new_marriage_to_have
                and wife_marriage.status not in valid_marriage_statuses_for_spouses_to_have
            ):
                raise ApplicationError(
                    message=PERSON_IS_MARRIED,
                    extra={"person_id": wife.id},
                )
