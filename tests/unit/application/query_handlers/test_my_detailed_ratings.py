from datetime import date, datetime, timezone
from unittest.mock import Mock

from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.readers.my_detailed_ratings import (
    MyDetailedRatingsViewModelReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.my_detailed_ratings import (
    MovieViewModel,
    RatingViewModel,
    DetailedRatingViewModel,
    MyDetailedRatingsViewModel,
)
from amdb.application.queries.my_detailed_ratings import (
    GetMyDetailedRatingsQuery,
)
from amdb.application.query_handlers.my_detailed_ratings import (
    GetMyDetailedRatingsHandler,
)


def test_get_my_detailed_ratings(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    my_detailed_ratings_reader: MyDetailedRatingsViewModelReader,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
        telegram=None,
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
    identity_provider.user_id = Mock(
        return_value=user.id,
    )

    query = GetMyDetailedRatingsQuery(
        limit=10,
        offset=0,
    )
    handler = GetMyDetailedRatingsHandler(
        my_detailed_ratings_reader=my_detailed_ratings_reader,
        identity_provider=identity_provider,
    )

    expected_result = MyDetailedRatingsViewModel(
        detailed_ratings=[
            DetailedRatingViewModel(
                movie=MovieViewModel(
                    id=movie.id,
                    title=movie.title,
                    release_date=movie.release_date,
                    rating=movie.rating,
                    rating_count=movie.rating_count,
                ),
                rating=RatingViewModel(
                    id=rating.id,
                    value=rating.value,
                    created_at=rating.created_at,
                ),
            ),
        ],
        rating_count=1,
    )
    result = handler.execute(query)

    assert expected_result == result
