from datetime import datetime, timezone
from typing import cast

from amdb.domain.entities.person.person import Person
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.delete_marriage import DeleteMarriage
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.person.delete_marriage import DeleteMarriageCommand
from amdb.application.common.constants.exceptions import (
    DELETE_MARRIAGE_ACCESS_DENIED,
    MARRIAGE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class DeleteMarriageHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        delete_marriage: DeleteMarriage,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._delete_marriage = delete_marriage
        self._access_policy_gateway = access_policy_gateway
        self._marriage_gateway = marriage_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: DeleteMarriageCommand) -> None:
        required_access_policy = self._access_policy_gateway.for_delete_marriage()
        current_access_policy = self._identity_provider.get_access_policy()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(DELETE_MARRIAGE_ACCESS_DENIED)

        marriage = self._marriage_gateway.with_id(
            marriage_id=command.marriage_id,
        )
        if marriage is None:
            raise ApplicationError(MARRIAGE_DOES_NOT_EXIST)

        husband = self._person_gateway.with_id(
            person_id=marriage.husband_id,
        )
        husband = cast(Person, husband)

        wife = self._person_gateway.with_id(
            person_id=marriage.wife_id,
        )
        wife = cast(Person, wife)

        children = self._person_gateway.list_with_ids(
            *marriage.child_ids,
        )
        children = cast(list[Person], children)

        self._delete_marriage(
            husband=husband,
            wife=wife,
            children=children,
            timestamp=datetime.now(timezone.utc),
        )
        self._marriage_gateway.delete(
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
