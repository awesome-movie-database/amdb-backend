from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.readers.review import ReviewViewModelReader
from amdb.application.common.view_models.review import ReviewViewModel
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.reviews import GetReviewsQuery


class GetReviewsHandler:
    def __init__(
        self,
        *,
        movie_gateway: MovieGateway,
        review_view_model_reader: ReviewViewModelReader,
    ) -> None:
        self._movie_gateway = movie_gateway
        self._review_view_model_reader = review_view_model_reader

    def execute(self, query: GetReviewsQuery) -> list[ReviewViewModel]:
        movie = self._movie_gateway.with_id(query.movie_id)
        if not movie:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        review_view_models = self._review_view_model_reader.list(
            movie_id=query.movie_id,
            limit=query.limit,
            offset=query.offset,
        )

        return review_view_models
