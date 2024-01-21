from unittest.mock import Mock

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movie import GetMovieQuery, GetMovieResult
from amdb.application.query_handlers.get_movie import GetMovieHandler
from amdb.application.common.constants.exceptions import (
    GET_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_movie(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    get_movie_query = GetMovieQuery(
        movie_id=movie.id,
    )
    get_movie_handler = GetMovieHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_movie_result = get_movie_handler.execute(get_movie_query)
    expected_get_movie_result = GetMovieResult(
        title=movie.title,
        rating=movie.rating,
        rating_count=movie.rating_count,
    )

    assert get_movie_result == expected_get_movie_result


def test_get_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_movie_query = GetMovieQuery(
        movie_id=MovieId(uuid7()),
    )
    get_movie_handler = GetMovieHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_movie_handler.execute(get_movie_query)

    assert error.value.message == GET_MOVIE_ACCESS_DENIED


def test_get_movie_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    get_movie_query = GetMovieQuery(
        movie_id=MovieId(uuid7()),
    )
    get_movie_handler = GetMovieHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_movie_handler.execute(get_movie_query)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
