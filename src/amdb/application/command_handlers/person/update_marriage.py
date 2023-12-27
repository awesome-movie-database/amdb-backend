from datetime import datetime, timezone
from typing import cast

from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import Marriage
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.update_marriage import Children, UpdateMarriage
from amdb.domain.constants.common import unset
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.person.update_marriage import UpdateMarriageCommand
from amdb.application.common.constants.exceptions import (
    UPDATE_MARRIAGE_INVALID_COMMAND,
    UPDATE_MARRIAGE_ACCESS_DENIED,
    MARRIAGE_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class UpdateMarriageHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        update_marriage: UpdateMarriage,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._update_marriage = update_marriage
        self._access_policy_gateway = access_policy_gateway
        self._marriage_gateway = marriage_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: UpdateMarriageCommand) -> None:
        required_access_policy = self._access_policy_gateway.for_update_marriage()
        current_access_policy = self._identity_provider.get_access_policy()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(UPDATE_MARRIAGE_ACCESS_DENIED)

        marriage = self._marriage_gateway.with_id(
            marriage_id=command.marriage_id,
        )
        if marriage is None:
            raise ApplicationError(MARRIAGE_DOES_NOT_EXIST)

        self._ensure_valid_command(
            command=command,
            marriage=marriage,
        )

        husband = self._person_gateway.with_id(
            person_id=marriage.husband_id,
        )
        husband = cast(Person, husband)

        wife = self._person_gateway.with_id(
            person_id=marriage.wife_id,
        )
        wife = cast(Person, wife)

        if command.child_ids is not unset:
            children, persons_to_update = self._get_children(
                marriage=marriage,
                child_ids=command.child_ids,
            )
        else:
            children = unset  # type: ignore[assignment]
            persons_to_update = []

        self._update_marriage(
            marriage=marriage,
            husband=husband,
            wife=wife,
            timestamp=datetime.now(timezone.utc),
            children=children,
            status=command.status,
            start_date=command.start_date,
            end_date=command.end_date,
        )
        self._marriage_gateway.update(
            marriage=marriage,
        )
        self._person_gateway.update(
            husband,
            wife,
            *persons_to_update,
        )

        self._unit_of_work.commit()

    def _ensure_valid_command(
        self,
        *,
        command: UpdateMarriageCommand,
        marriage: Marriage,
    ) -> None:
        if command.child_ids is not unset and (
            marriage.husband_id in command.child_ids or marriage.wife_id in command.child_ids
        ):
            raise ApplicationError(
                message=UPDATE_MARRIAGE_INVALID_COMMAND,
                extra={"details": "Child ids contain id of husband or wife"},
            )

    def _get_children(
        self,
        *,
        marriage: Marriage,
        child_ids: list[PersonId],
    ) -> tuple[Children, list[Person]]:
        total_child_ids = set()
        for marriage_child_id in marriage.child_ids:
            total_child_ids.add(marriage_child_id)
        for child_id in child_ids:
            total_child_ids.add(child_id)

        children, missing_child_ids = self._person_gateway.list_with_ids(
            *total_child_ids,
        )
        if missing_child_ids:
            raise ApplicationError(
                message=PERSONS_DO_NOT_EXIST,
                extra={"person_ids": missing_child_ids},
            )

        old_children, new_children = [], []
        for child in children:
            if child.id in marriage.child_ids:
                old_children.append(child)
            elif child.id in child_ids:
                new_children.append(child)

        return (
            Children(
                old_children=old_children,
                new_children=new_children,
            ),
            children,
        )
