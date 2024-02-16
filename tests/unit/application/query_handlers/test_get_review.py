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
from amdb.application.queries.get_review import GetReviewQuery, GetReviewResult
from amdb.application.query_handlers.get_review import GetReviewHandler
from amdb.application.common.constants.exceptions import (
    GET_REVIEW_ACCESS_DENIED,
    REVIEW_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_review()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_review(
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

    get_review_query = GetReviewQuery(
        review_id=review.id,
    )
    get_review_handler = GetReviewHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_review_result = get_review_handler.execute(get_review_query)
    expected_get_review_result = GetReviewResult(
        user_id=review.user_id,
        movie_id=review.movie_id,
        title=review.title,
        content=review.content,
        type=review.type,
        created_at=review.created_at,
    )

    assert get_review_result == expected_get_review_result


def test_get_review_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    review_gateway: ReviewGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_review_query = GetReviewQuery(
        review_id=ReviewId(uuid7()),
    )
    get_review_handler = GetReviewHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_review_handler.execute(get_review_query)

    assert error.value.message == GET_REVIEW_ACCESS_DENIED


def test_get_review_should_raise_error_when_review_does_not_exist(
    permissions_gateway: PermissionsGateway,
    review_gateway: ReviewGateway,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    get_review_query = GetReviewQuery(
        review_id=ReviewId(uuid7()),
    )
    get_review_handler = GetReviewHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_review_handler.execute(get_review_query)

    assert error.value.message == REVIEW_DOES_NOT_EXIST
