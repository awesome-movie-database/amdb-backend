from unittest.mock import Mock
from datetime import date

import pytest

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_movie import CreateMovie
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.create_movie import CreateMovieCommand
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.common.constants.exceptions import (
    CREATE_MOVIE_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_create_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_create_movie(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    create_movie_command = CreateMovieCommand(
        title="Matrix",
        release_date=date(1999, 3, 31),
    )
    create_movie_handler = CreateMovieHandler(
        access_concern=AccessConcern(),
        create_movie=CreateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    create_movie_handler.execute(create_movie_command)


def test_create_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    create_movie_command = CreateMovieCommand(
        title="Matrix",
        release_date=date(1999, 3, 31),
    )
    create_movie_handler = CreateMovieHandler(
        access_concern=AccessConcern(),
        create_movie=CreateMovie(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        create_movie_handler.execute(create_movie_command)

    assert error.value.message == CREATE_MOVIE_ACCESS_DENIED
