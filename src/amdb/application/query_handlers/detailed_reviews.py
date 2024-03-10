from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.readers.detailed_review import (
    DetailedReviewViewModelsReader,
)
from amdb.application.common.view_models.detailed_review import (
    DetailedReviewViewModel,
)
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.detailed_reviews import GetDetailedReviewsQuery


class GetDetailedReviewsHandler:
    def __init__(
        self,
        *,
        movie_gateway: MovieGateway,
        detailed_reviews_reader: DetailedReviewViewModelsReader,
    ) -> None:
        self._movie_gateway = movie_gateway
        self._detailed_reviews_reader = detailed_reviews_reader

    def execute(
        self,
        query: GetDetailedReviewsQuery,
    ) -> list[DetailedReviewViewModel]:
        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        view_models = self._detailed_reviews_reader.get(
            movie_id=query.movie_id,
            limit=query.limit,
            offset=query.offset,
        )

        return view_models
