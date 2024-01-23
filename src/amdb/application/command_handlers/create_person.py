from uuid_extensions import uuid7

from amdb.domain.entities.person import PersonId
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_person import CreatePerson
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.person_gateway import PersonGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import CREATE_PERSON_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.create_person import CreatePersonCommand


class CreatePersonHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        create_person: CreatePerson,
        permissions_gateway: PermissionsGateway,
        person_gateway: PersonGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._access_concern = access_concern
        self._create_person = create_person
        self._permissions_gateway = permissions_gateway
        self._person_gateway = person_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: CreatePersonCommand) -> PersonId:
        current_permissions = self._identity_provider.get_permissions()
        required_permissions = self._permissions_gateway.for_create_person()
        access = self._access_concern.authorize(
            current_permissions=current_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(CREATE_PERSON_ACCESS_DENIED)

        person = self._create_person(
            id=PersonId(uuid7()),
            name=command.name,
        )
        self._person_gateway.save(person)

        self._unit_of_work.commit()

        return person.id
