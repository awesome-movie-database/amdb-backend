from unittest.mock import Mock

import pytest

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_movie import CreateMovie
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.common.constants.exceptions import CREATE_MOVIE_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.fixture(scope="module")
def identity_provider_with_valid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_permissions = Mock(
        return_value=2,
    )

    return identity_provider


@pytest.fixture(scope="module")
def identity_provider_with_invalid_permissions() -> IdentityProvider:
    identity_provider = Mock()
    identity_provider.get_permissions = Mock(
        return_value=4,
    )

    return identity_provider


def test_create_movie(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_valid_permissions: IdentityProvider,
):
    create_movie_command = CreateMovieCommand(
        title="Matrix",
    )
    create_movie_handler = CreateMovieHandler(
        access_concern=AccessConcern(),
        create_movie=CreateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_valid_permissions,
    )

    create_movie_handler.execute(create_movie_command)


def test_create_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_invalid_permissions: IdentityProvider,
):
    create_movie_command = CreateMovieCommand(
        title="Matrix",
    )
    create_movie_handler = CreateMovieHandler(
        access_concern=AccessConcern(),
        create_movie=CreateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_invalid_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        create_movie_handler.execute(create_movie_command)

    assert error.value.message == CREATE_MOVIE_ACCESS_DENIED
