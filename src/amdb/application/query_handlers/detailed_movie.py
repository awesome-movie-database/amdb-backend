from amdb.application.common.readers.detailed_movie import (
    DetailedMovieViewModelReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.constants.exceptions import MOVIE_DOES_NOT_EXIST
from amdb.application.common.exception import ApplicationError
from amdb.application.common.view_models.detailed_movie import (
    DetailedMovieViewModel,
)
from amdb.application.queries.detailed_movie import GetDetailedMovieQuery


class GetDetailedMovieHandler:
    def __init__(
        self,
        *,
        detailed_movie_reader: DetailedMovieViewModelReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._detailed_movie_reader = detailed_movie_reader
        self._identity_provider = identity_provider

    def execute(self, query: GetDetailedMovieQuery) -> DetailedMovieViewModel:
        current_user_id = self._identity_provider.user_id_or_none()

        detailed_movie_view_model = self._detailed_movie_reader.one(
            movie_id=query.movie_id,
            current_user_id=current_user_id,
        )
        if not detailed_movie_view_model:
            raise ApplicationError(MOVIE_DOES_NOT_EXIST)

        return detailed_movie_view_model
