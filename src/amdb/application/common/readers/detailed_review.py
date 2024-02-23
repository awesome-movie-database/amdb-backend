from typing import Protocol

from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.detailed_review import (
    DetailedReviewViewModel,
)


class DetailedReviewViewModelReader(Protocol):
    def list(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[DetailedReviewViewModel]:
        raise NotImplementedError
