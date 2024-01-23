from unittest.mock import Mock

import pytest

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_person import CreatePerson
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.person_gateway import PersonGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_person import CreatePersonCommand
from amdb.application.command_handlers.create_person import CreatePersonHandler
from amdb.application.common.constants.exceptions import CREATE_PERSON_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_create_person()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_create_person(
    permissions_gateway: PermissionsGateway,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    create_person_command = CreatePersonCommand(
        name="David Lynch",
    )
    create_person_handler = CreatePersonHandler(
        access_concern=AccessConcern(),
        create_person=CreatePerson(),
        permissions_gateway=permissions_gateway,
        person_gateway=person_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    create_person_handler.execute(create_person_command)


def test_create_person_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    person_gateway: PersonGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    create_person_command = CreatePersonCommand(
        name="David Lynch",
    )
    create_person_handler = CreatePersonHandler(
        access_concern=AccessConcern(),
        create_person=CreatePerson(),
        permissions_gateway=permissions_gateway,
        person_gateway=person_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        create_person_handler.execute(create_person_command)

    assert error.value.message == CREATE_PERSON_ACCESS_DENIED
