from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.readers.movie import MovieViewModelReader
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.non_detailed_movie import (
    UserRating,
    NonDetailedMovieViewModel,
)
from amdb.application.queries.non_detailed_movies import GetNonDetailedMoviesQuery
from amdb.application.query_handlers.non_detailed_movies import GetNonDetailedMoviesHandler
from amdb.application.common.constants.exceptions import GET_MOVIE_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_movie()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_non_detailed_movies(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    permissions_gateway: PermissionsGateway,
    movie_view_model_reader: MovieViewModelReader,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=8,
        rating_count=1,
    )
    movie_gateway.save(movie)

    rating = Rating(
        id=RatingId(uuid7()),
        movie_id=movie.id,
        user_id=user.id,
        value=8,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

    get_non_detailed_movies_query = GetNonDetailedMoviesQuery(
        limit=10,
        offset=0,
    )
    get_non_detailed_movies_handler = GetNonDetailedMoviesHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_view_model_reader=movie_view_model_reader,
        identity_provider=identity_provider_with_correct_permissions,
    )

    expected_result = [
            NonDetailedMovieViewModel(
            id=movie.id,
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            user_rating=UserRating(
                id=rating.id,
                value=rating.value,
            ),
        ),
    ]
    result = get_non_detailed_movies_handler.execute(get_non_detailed_movies_query)

    assert expected_result == result


def test_get_non_detailed_movies_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_view_model_reader: MovieViewModelReader,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_non_detailed_movies_query = GetNonDetailedMoviesQuery(
        limit=10,
        offset=0,
    )
    get_non_detailed_movies_handler = GetNonDetailedMoviesHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_view_model_reader=movie_view_model_reader,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_non_detailed_movies_handler.execute(get_non_detailed_movies_query)

    assert error.value.message == GET_MOVIE_ACCESS_DENIED
