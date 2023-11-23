from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import RatingType


@dataclass(slots=True)
class SeriesSeasonReviewRating(Entity):
    series_id: UUID
    season: int
    reviewer_id: UUID
    type: RatingType
    created_at: datetime

    @classmethod
    def create(
        cls,
        series_id: UUID,
        season: int,
        reviewer_id: UUID,
        type: RatingType,
        created_at: datetime,
    ) -> "SeriesSeasonReviewRating":
        return SeriesSeasonReviewRating(
            series_id=series_id,
            season=season,
            reviewer_id=reviewer_id,
            type=type,
            created_at=created_at,
        )

    def change_type(self, rating_type: RatingType) -> None:
        self.type = rating_type
