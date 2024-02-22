from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.readers.review import ReviewViewModelReader
from amdb.application.common.view_models.review import (
    UserRating,
    UserReview,
    ReviewViewModel,
)
from amdb.application.queries.reviews import GetReviewsQuery
from amdb.application.query_handlers.reviews import GetReviewsHandler
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError


def test_get_reviews(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    review_reader: ReviewViewModelReader,
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

    review = Review(
        id=ReviewId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        title="Not bad",
        content="Great soundtrack",
        type=ReviewType.POSITIVE,
        created_at=datetime.now(timezone.utc),
    )
    review_gateway.save(review)

    unit_of_work.commit()

    get_reviews_query = GetReviewsQuery(
        movie_id=movie.id,
        limit=10,
        offset=0,
    )
    get_reviews_handler = GetReviewsHandler(
        movie_gateway=movie_gateway,
        review_view_model_reader=review_reader,
    )

    expected_result = [
        ReviewViewModel(
            user_id=user.id,
            user_review=UserReview(
                id=review.id,
                title=review.title,
                content=review.content,
                type=review.type,
                created_at=review.created_at,
            ),
            user_rating=UserRating(
                id=rating.id,
                value=rating.value,
                created_at=rating.created_at,
            ),
        ),
    ]
    result = get_reviews_handler.execute(get_reviews_query)

    assert expected_result == result


def test_get_reviews_should_raise_error_when_movie_does_not_exist(
    movie_gateway: MovieGateway,
    review_reader: ReviewViewModelReader,
):
    get_reviews_query = GetReviewsQuery(
        movie_id=MovieId(uuid7()),
        limit=10,
        offset=0,
    )
    get_reviews_handler = GetReviewsHandler(
        movie_gateway=movie_gateway,
        review_view_model_reader=review_reader,
    )

    with pytest.raises(ApplicationError) as error:
        get_reviews_handler.execute(get_reviews_query)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
