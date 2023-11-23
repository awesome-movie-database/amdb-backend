from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import RatingType


@dataclass(slots=True)
class SeriesEpisodeReviewRating(Entity):
    series_id: UUID
    episode: int
    reviewer_id: UUID
    type: RatingType
    created_at: datetime

    @classmethod
    def create(
        cls,
        series_id: UUID,
        episode: int,
        reviewer_id: UUID,
        type: RatingType,
        created_at: datetime,
    ) -> "SeriesEpisodeReviewRating":
        return SeriesEpisodeReviewRating(
            series_id=series_id,
            episode=episode,
            reviewer_id=reviewer_id,
            type=type,
            created_at=created_at,
        )

    def change_type(self, rating_type: RatingType) -> None:
        self.type = rating_type
