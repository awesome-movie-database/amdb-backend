from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.person.person import PersonId
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_person import CreatePerson
from amdb.application.commands.person.create_person import CreatePersonCommand
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import CREATE_PERSON_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


class CreatePersonHandler:
    def __init__(
        self,
        access_concern: AccessConcern,
        create_person: CreatePerson,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._create_person = create_person
        self._access_policy_gateway = access_policy_gateway
        self._person_gateway = person_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: CreatePersonCommand) -> PersonId:
        required_access_policy = self._access_policy_gateway.for_create_person()
        current_access_policy = self._identity_provider.get_access_policy()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(CREATE_PERSON_ACCESS_DENIED)

        person = self._create_person(
            id=PersonId(uuid4()),
            name=command.name,
            sex=command.sex,
            timestamp=datetime.now(timezone.utc),
            birth_date=command.birth_date,
            birth_place=command.birth_place,
            death_date=command.death_date,
            death_place=command.death_place,
        )
        self._person_gateway.save(
            person=person,
        )

        self._unit_of_work.commit()

        return person.id
