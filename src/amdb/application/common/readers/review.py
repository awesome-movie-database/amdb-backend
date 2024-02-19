from typing import Protocol

from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.review import ReviewViewModel


class ReviewViewModelReader(Protocol):
    def list(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[ReviewViewModel]:
        raise NotImplementedError
