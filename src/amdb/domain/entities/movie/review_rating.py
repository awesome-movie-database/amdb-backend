from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import RatingType


@dataclass(slots=True)
class MovieReviewRating(Entity):

    movie_id: UUID
    reviewer_id: UUID
    type: RatingType
    created_at: datetime

    @classmethod
    def create(
        cls, movie_id: UUID, reviewer_id: UUID,
        type: RatingType, created_at: datetime,
    ) -> "MovieReviewRating":
        return MovieReviewRating(
            movie_id=movie_id, reviewer_id=reviewer_id,
            type=type, created_at=created_at,
        )

    def change_type(self, rating_type: RatingType) -> None:
        self.type = rating_type
