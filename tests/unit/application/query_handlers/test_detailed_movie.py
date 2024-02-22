from unittest.mock import Mock
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
from amdb.application.common.readers.detailed_movie import (
    DetailedMovieViewModelReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.detailed_movie import (
    UserRating,
    UserReview,
    DetailedMovieViewModel,
)
from amdb.application.queries.detailed_movie import GetDetailedMovieQuery
from amdb.application.query_handlers.detailed_movie import (
    GetDetailedMovieHandler,
)
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError


def test_get_detailed_movie(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    detailed_movie_reader: DetailedMovieViewModelReader,
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

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id_or_none = Mock(
        return_value=user.id,
    )

    get_detailed_movie_query = GetDetailedMovieQuery(
        movie_id=movie.id,
    )
    get_detailed_movie_handler = GetDetailedMovieHandler(
        detailed_movie_reader=detailed_movie_reader,
        identity_provider=identity_provider,
    )

    expected_result = DetailedMovieViewModel(
        id=movie.id,
        title=movie.title,
        release_date=movie.release_date,
        rating=movie.rating,
        rating_count=movie.rating_count,
        user_rating=UserRating(
            id=rating.id,
            value=rating.value,
            created_at=rating.created_at,
        ),
        user_review=UserReview(
            id=review.id,
            title=review.title,
            content=review.content,
            type=review.type,
            created_at=review.created_at,
        ),
    )
    result = get_detailed_movie_handler.execute(get_detailed_movie_query)

    assert expected_result == result


def test_get_detailed_movie_should_raise_error_when_movie_does_not_exist(
    detailed_movie_reader: DetailedMovieViewModelReader,
):
    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id_or_none = Mock(
        return_value=None,
    )

    get_detailed_movie_query = GetDetailedMovieQuery(
        movie_id=MovieId(uuid7()),
    )
    get_detailed_movie_handler = GetDetailedMovieHandler(
        detailed_movie_reader=detailed_movie_reader,
        identity_provider=identity_provider,
    )

    with pytest.raises(ApplicationError) as error:
        get_detailed_movie_handler.execute(get_detailed_movie_query)

    assert error.value.message == MOVIE_DOES_NOT_EXIST
