from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import (
    PermissionsGateway,
)
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.review_gateway import ReviewGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_my_reviews import (
    GetMyReviewsQuery,
    GetMyReviewsResult,
)
from amdb.application.query_handlers.get_my_reviews import GetMyReviewsHandler
from amdb.application.common.constants.exceptions import (
    GET_MY_REVIEWS_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_my_reviews()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_my_reviews(
    permissions_gateway: PermissionsGateway,
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    review_gateway: ReviewGateway,
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
        title="Gone girl",
        release_date=date(2014, 10, 3),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    review = Review(
        id=ReviewId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        title="Masterpice",
        content="Extremely underrated",
        type=ReviewType.POSITIVE,
        created_at=datetime.now(timezone.utc),
    )
    review_gateway.save(review)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.get_user_id = Mock(
        return_value=user.id,
    )

    get_my_reviews_query = GetMyReviewsQuery(
        limit=10,
        offset=0,
    )
    get_my_reviews_handler = GetMyReviewsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_my_reviews_result = get_my_reviews_handler.execute(
        get_my_reviews_query
    )
    expected_get_my_reviews_result = GetMyReviewsResult(
        reviews=[review],
        review_count=1,
    )

    assert get_my_reviews_result == expected_get_my_reviews_result


def test_get_my_reviews_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    review_gateway: ReviewGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_my_reviews_query = GetMyReviewsQuery(
        limit=10,
        offset=0,
    )
    get_my_reviews_handler = GetMyReviewsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    identity_provider_with_incorrect_permissions.get_user_id = Mock(
        return_value=UserId(uuid7()),
    )

    with pytest.raises(ApplicationError) as error:
        get_my_reviews_handler.execute(get_my_reviews_query)

    assert error.value.message == GET_MY_REVIEWS_ACCESS_DENIED
