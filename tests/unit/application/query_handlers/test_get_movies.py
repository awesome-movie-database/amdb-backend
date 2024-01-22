from unittest.mock import Mock

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movies import GetMoviesQuery, GetMoviesResult
from amdb.application.query_handlers.get_movies import GetMoviesHandler
from amdb.application.common.constants.exceptions import GET_MOVIES_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_movies()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_movies(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    movie1 = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie1)

    movie2 = Movie(
        id=MovieId(uuid7()),
        title="There Will Be Blood",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie2)

    movie3 = Movie(
        id=MovieId(uuid7()),
        title="Mulholland Drive",
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie3)

    unit_of_work.commit()

    get_movies_query = GetMoviesQuery(
        limit=10,
        offset=1,
    )
    get_movies_handler = GetMoviesHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_movies_result = get_movies_handler.execute(get_movies_query)
    expected_get_movies_result = GetMoviesResult(
        movies=[movie2, movie3],
        movie_count=2,
    )

    assert get_movies_result == expected_get_movies_result


def test_get_movies_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_movies_query = GetMoviesQuery(
        limit=10,
        offset=1,
    )
    get_movies_handler = GetMoviesHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_movies_handler.execute(get_movies_query)

    assert error.value.message == GET_MOVIES_ACCESS_DENIED
