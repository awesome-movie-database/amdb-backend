from amdb.application.common.readers.non_detailed_movie import (
    NonDetailedMovieViewModelsReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.non_detailed_movie import (
    NonDetailedMovieViewModel,
)
from amdb.application.queries.non_detailed_movies import (
    GetNonDetailedMoviesQuery,
)


class GetNonDetailedMoviesHandler:
    def __init__(
        self,
        *,
        non_detailed_movies_reader: NonDetailedMovieViewModelsReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._non_detailed_movies_reader = non_detailed_movies_reader
        self._identity_provider = identity_provider

    def execute(
        self,
        query: GetNonDetailedMoviesQuery,
    ) -> list[NonDetailedMovieViewModel]:
        current_user_id = self._identity_provider.user_id_or_none()

        view_models = self._non_detailed_movies_reader.get(
            current_user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )

        return view_models
