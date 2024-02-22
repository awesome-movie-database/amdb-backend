from typing import Protocol, Optional

from amdb.domain.entities.user import UserId
from amdb.application.common.view_models.non_detailed_movie import (
    NonDetailedMovieViewModel,
)


class NonDetailedMovieViewModelReader(Protocol):
    def list(
        self,
        current_user_id: Optional[UserId],
        limit: int,
        offset: int,
    ) -> list[NonDetailedMovieViewModel]:
        raise NotImplementedError
