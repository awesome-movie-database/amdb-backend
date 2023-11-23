from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.value_objects import Vote


@dataclass(slots=True)
class SeriesEpisodeVote(Entity):
    series_id: UUID
    episode: int
    reviewer_id: UUID
    vote: Vote
    is_full: bool
    created_at: datetime

    updated_at: Optional[datetime]

    @classmethod
    def create(
        cls,
        series_id: UUID,
        episode: int,
        reviewer_id: UUID,
        vote: Vote,
        is_full: bool,
        created_at: datetime,
    ) -> "SeriesEpisodeVote":
        return SeriesEpisodeVote(
            series_id=series_id,
            episode=episode,
            reviewer_id=reviewer_id,
            vote=vote,
            is_full=is_full,
            created_at=created_at,
            updated_at=None,
        )

    def change_vote(self, vote: Vote, updated_at: datetime) -> None:
        self.vote = vote
        self.updated_at = updated_at

    def make_full(self) -> None:
        self.is_full = True
