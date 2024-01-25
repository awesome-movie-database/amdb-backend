from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_rating import GetRatingQuery, GetRatingResult
from amdb.application.query_handlers.get_rating import GetRatingHandler
from amdb.application.common.constants.exceptions import (
    GET_RATING_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_NOT_RATED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_rating()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_rating(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
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
        rating=10,
        rating_count=1,
    )
    movie_gateway.save(movie)

    rating = Rating(
        movie_id=movie.id,
        user_id=user.id,
        value=10,
        created_at=datetime.now(timezone.utc),
    )
    rating_gateway.save(rating)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

    get_rating_query = GetRatingQuery(
        movie_id=movie.id,
    )
    get_rating_handler = GetRatingHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_rating_result = get_rating_handler.execute(get_rating_query)
    expected_get_rating_result = GetRatingResult(
        value=rating.value,
        created_at=rating.created_at,
    )

    assert get_rating_result == expected_get_rating_result


def test_get_rating_should_raise_error_when_access_is_denied(
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    permissions_gateway: PermissionsGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_rating_query = GetRatingQuery(
        movie_id=MovieId(uuid7()),
    )
    get_rating_handler = GetRatingHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_rating_handler.execute(get_rating_query)

    assert error.value.message == GET_RATING_ACCESS_DENIED


def test_get_rating_should_raise_error_when_movie_does_not_exist(
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    permissions_gateway: PermissionsGateway,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    get_rating_query = GetRatingQuery(
        movie_id=MovieId(uuid7()),
    )
    get_rating_handler = GetRatingHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_rating_handler.execute(get_rating_query)

    assert error.value.message == MOVIE_DOES_NOT_EXIST


def test_get_rating_should_raise_error_when_movie_is_not_rated(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
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
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

    get_rating_query = GetRatingQuery(
        movie_id=movie.id,
    )
    get_rating_handler = GetRatingHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_rating_handler.execute(get_rating_query)

    assert error.value.message == MOVIE_NOT_RATED
