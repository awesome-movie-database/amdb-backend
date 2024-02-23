from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.readers.detailed_review import (
    DetailedReviewViewModelReader,
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
        detailed_review_reader: DetailedReviewViewModelReader,
    ) -> None:
        self._movie_gateway = movie_gateway
        self._detailed_review_reader = detailed_review_reader

    def execute(
        self,
        query: GetDetailedReviewsQuery,
    ) -> list[DetailedReviewViewModel]:
        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        review_view_models = self._detailed_review_reader.list(
            movie_id=query.movie_id,
            limit=query.limit,
            offset=query.offset,
        )

        return review_view_models
