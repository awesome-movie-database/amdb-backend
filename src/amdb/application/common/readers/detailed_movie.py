from typing import Protocol, Optional

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.detailed_movie import (
    DetailedMovieViewModel,
)


class DetailedMovieViewModelReader(Protocol):
    def one(
        self,
        movie_id: MovieId,
        current_user_id: Optional[UserId],
    ) -> Optional[DetailedMovieViewModel]:
        raise NotImplementedError
