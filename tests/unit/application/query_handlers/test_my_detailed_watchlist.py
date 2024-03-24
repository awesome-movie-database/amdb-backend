from unittest.mock import Mock
from datetime import date, datetime, timezone

from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.entities.movie import Movie, MovieId
from amdb.domain.entities.movie_for_later import MovieForLater, MovieForLaterId
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.movie_for_later import (
    MovieForLaterGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.readers.my_detailed_watchlist import (
    MyDetailedWatchlistViewModelReader,
)
from amdb.application.common.view_models.my_detailed_watchlist import (
    MovieViewModel,
    MovieForLaterViewModel,
    DetailedMovieForLaterViewModel,
    MyDetailedWatchlistViewModel,
)
from amdb.application.queries.my_detailed_watchlist import (
    GetMyDeatiledWatchlistQuery,
)
from amdb.application.query_handlers.my_detailed_watchlist import (
    GetMyDetailedWatchlistHandler,
)


def test_get_my_detailed_watchlist(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    movie_for_later_gateway: MovieForLaterGateway,
    unit_of_work: UnitOfWork,
    my_detailed_watchlist_reader: MyDetailedWatchlistViewModelReader,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="john@doe.com",
        telegram=None,
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

    movie_for_later = MovieForLater(
        id=MovieForLaterId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        note="Movie with Keanu Reeves that i saw on TV",
        created_at=datetime.now(timezone.utc),
    )
    movie_for_later_gateway.save(movie_for_later)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(
        return_value=user.id,
    )

    query = GetMyDeatiledWatchlistQuery(
        limit=10,
        offset=0,
    )
    handler = GetMyDetailedWatchlistHandler(
        my_detailed_watchlist_reader=my_detailed_watchlist_reader,
        identity_provider=identity_provider,
    )

    expected_result = MyDetailedWatchlistViewModel(
        detailed_movies_for_later=[
            DetailedMovieForLaterViewModel(
                movie=MovieViewModel(
                    id=movie.id,
                    title=movie.title,
                    release_date=movie.release_date,
                    rating=movie.rating,
                    rating_count=movie.rating_count,
                ),
                movie_for_later=MovieForLaterViewModel(
                    id=movie_for_later.id,
                    note=movie_for_later.note,
                    created_at=movie_for_later.created_at,
                ),
            ),
        ],
        movie_for_later_count=1,
    )
    result = handler.execute(query)

    assert expected_result == result
