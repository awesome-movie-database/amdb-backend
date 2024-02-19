from typing import Protocol, Optional

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.detailed_movie import (
    DetailedMovieViewModel,
)
from amdb.application.common.view_models.non_detailed_movie import (
    NonDetailedMovieViewModel,
)


class MovieViewModelReader(Protocol):
    def list_non_detailed(
        self,
        current_user_id: Optional[UserId],
        limit: int,
        offset: int,
    ) -> list[NonDetailedMovieViewModel]:
        raise NotImplementedError

    def detailed(
        self,
        movie_id: MovieId,
        current_user_id: Optional[UserId],
    ) -> Optional[DetailedMovieViewModel]:
        raise NotImplementedError
