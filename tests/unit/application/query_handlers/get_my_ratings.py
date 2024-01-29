from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_my_ratings import GetMyRatingsQuery, GetMyRatingsResult
from amdb.application.query_handlers.get_my_ratings import GetMyRatingsHandler
from amdb.application.common.constants.exceptions import GET_MY_RATINGS_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_my_ratings()
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
        id=RatingId(uuid7()),
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

    get_my_ratings_query = GetMyRatingsQuery(
        limit=10,
        offset=0,
    )
    get_my_ratings_handler = GetMyRatingsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_my_ratings_result = get_my_ratings_handler.execute(get_my_ratings_query)
    expected_get_my_ratings_result = GetMyRatingsResult(
        ratings=[rating],
        rating_count=1,
    )

    assert get_my_ratings_result == expected_get_my_ratings_result


def test_get_rating_should_raise_error_when_access_is_denied(
    rating_gateway: RatingGateway,
    permissions_gateway: PermissionsGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_my_ratings_query = GetMyRatingsQuery(
        limit=10,
        offset=0,
    )
    get_my_ratings_handler = GetMyRatingsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        rating_gateway=rating_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_my_ratings_handler.execute(get_my_ratings_query)

    assert error.value.message == GET_MY_RATINGS_ACCESS_DENIED
