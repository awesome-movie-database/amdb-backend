from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import ReviewType


@dataclass(slots=True)
class SeriesEpisodeReview(Entity):
    series_id: UUID
    episode: int
    reviewer_id: UUID
    type: ReviewType
    title: str
    content: str
    likes: int
    dislikes: int
    is_approved: bool
    created_at: datetime

    @classmethod
    def create(
        cls,
        series_id: UUID,
        episode: int,
        review_id: UUID,
        type: ReviewType,
        title: str,
        content: str,
        is_approved: bool,
        created_at: datetime,
    ) -> "SeriesEpisodeReview":
        return SeriesEpisodeReview(
            series_id=series_id,
            episode=episode,
            reviewer_id=review_id,
            type=type,
            title=title,
            content=content,
            likes=0,
            dislikes=0,
            is_approved=is_approved,
            created_at=created_at,
        )

    def add_like(self) -> None:
        self.likes += 1

    def add_dislikes(self) -> None:
        self.dislikes += 1
