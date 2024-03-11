from datetime import date, datetime, timezone
from unittest.mock import Mock

from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.entities.movie import Movie, MovieId
from amdb.domain.entities.rating import Rating, RatingId
from amdb.application.common.services.convert_to_file import (
    ConvertMyRatingsToFile,
)
from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.readers.rating_for_export import (
    RatingForExportViewModelsReader,
)
from amdb.infrastructure.converting.ratings_for_export import (
    RealRatingsForExportConverter,
)
from amdb.application.queries.export_my_ratings import ExportMyRatingsQuery
from amdb.application.query_handlers.export_my_ratings import (
    ExportMyRatingsHandler,
)


def test_export_my_ratings_in_csv(
    user_gateway: UserGateway,
    movie_gateway: MovieGateway,
    rating_gateway: RatingGateway,
    unit_of_work: UnitOfWork,
    ratings_for_export_reader: RatingForExportViewModelsReader,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
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
    identity_provider.user_id = Mock(
        return_value=user.id,
    )

    query = ExportMyRatingsQuery(format=ExportFormat.CSV)
    handler = ExportMyRatingsHandler(
        convert_my_ratings_to_file=ConvertMyRatingsToFile(
            converter=RealRatingsForExportConverter(),
        ),
        ratings_for_export_reader=ratings_for_export_reader,
        identity_provider=identity_provider,
    )

    handler.execute(query)
