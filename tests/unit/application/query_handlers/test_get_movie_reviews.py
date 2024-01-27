from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.application.common.interfaces.review_gateway import ReviewGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movie_reviews import GetMovieReviewsQuery, GetMovieReviewsResult
from amdb.application.query_handlers.get_movie_reviews import GetMovieReviewsHandler
from amdb.application.common.constants.exceptions import (
    GET_MOVIE_REVIEWS_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_get_movie_reviews()
    identity_provider.get_permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_get_movie_reviews(
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

    get_movie_reviews_query = GetMovieReviewsQuery(
        movie_id=movie.id,
        limit=10,
        offset=0,
    )
    get_movie_reviews_handler = GetMovieReviewsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    get_movie_reviews_result = get_movie_reviews_handler.execute(get_movie_reviews_query)
    expected_get_movie_reviews_result = GetMovieReviewsResult(
        reviews=[review],
        review_count=1,
    )

    assert get_movie_reviews_result == expected_get_movie_reviews_result


def test_get_movie_reviews_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    review_gateway: ReviewGateway,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    get_movie_reviews_query = GetMovieReviewsQuery(
        movie_id=MovieId(uuid7()),
        limit=10,
        offset=0,
    )
    get_movie_reviews_handler = GetMovieReviewsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_movie_reviews_handler.execute(get_movie_reviews_query)

    assert error.value.message == GET_MOVIE_REVIEWS_ACCESS_DENIED


def test_get_movie_reviews_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    review_gateway: ReviewGateway,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    get_movie_reviews_query = GetMovieReviewsQuery(
        movie_id=MovieId(uuid7()),
        limit=10,
        offset=0,
    )
    get_movie_reviews_handler = GetMovieReviewsHandler(
        access_concern=AccessConcern(),
        permissions_gateway=permissions_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        get_movie_reviews_handler.execute(get_movie_reviews_query)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
