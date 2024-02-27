from unittest.mock import Mock
from datetime import date, datetime, timezone

from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.readers.non_detailed_movie import (
    NonDetailedMovieViewModelsReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.non_detailed_movie import (
    MovieViewModel,
    UserRatingViewModel,
    NonDetailedMovieViewModel,
)
from amdb.application.queries.non_detailed_movies import (
    GetNonDetailedMoviesQuery,
)
from amdb.application.query_handlers.non_detailed_movies import (
    GetNonDetailedMoviesHandler,
)


def test_get_non_detailed_movies(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    non_detailed_movies_reader: NonDetailedMovieViewModelsReader,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email="John@doe.com",
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

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id_or_none = Mock(
        return_value=user.id,
    )

    query = GetNonDetailedMoviesQuery(
        limit=10,
        offset=0,
    )
    handler = GetNonDetailedMoviesHandler(
        non_detailed_movies_reader=non_detailed_movies_reader,
        identity_provider=identity_provider,
    )

    expected_result = [
        NonDetailedMovieViewModel(
            movie=MovieViewModel(
                id=movie.id,
                title=movie.title,
                release_date=movie.release_date,
                rating=movie.rating,
            ),
            user_rating=UserRatingViewModel(
                id=rating.id,
                value=rating.value,
            ),
        ),
    ]
    result = handler.execute(query)

    assert expected_result == result
