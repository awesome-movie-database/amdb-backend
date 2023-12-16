from datetime import datetime, timezone

from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.update_person import UpdatePerson
from amdb.application.commands.person.update_person import UpdatePersonCommand
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    UPDATE_PERSON_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class UpdatePersonHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        update_person: UpdatePerson,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._update_person = update_person
        self._access_policy_gateway = access_policy_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: UpdatePersonCommand) -> None:
        current_access_policy = self._identity_provider.get_access_policy()
        required_access_policy = self._access_policy_gateway.for_update_person()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(UPDATE_PERSON_ACCESS_DENIED)

        person = self._person_gateway.with_id(
            person_id=command.person_id,
        )
        if person is None:
            raise ApplicationError(PERSON_DOES_NOT_EXIST)

        self._update_person(
            person=person,
            timestamp=datetime.now(timezone.utc),
            name=command.name,
            sex=command.sex,
            birth_date=command.birth_date,
            birth_place=command.birth_place,
            death_date=command.death_date,
            death_place=command.death_place,
        )
        self._person_gateway.update(
            person=person,
        )

        self._unit_of_work.commit()
