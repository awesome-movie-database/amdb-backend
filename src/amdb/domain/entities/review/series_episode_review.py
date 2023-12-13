from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants.common import ReviewType


SeriesEpisodeReviewId = NewType("SeriesEpisodeReviewId", UUID)


@dataclass(slots=True)
class SeriesEpisodeReview(Entity):
    id: SeriesEpisodeReviewId
    series_id: SeriesId
    season_number: int
    episode_number: int
    user_id: UserId
    type: ReviewType
    title: str
    content: str
    likes: int
    dislikes: int
    is_approved: bool
    created_at: datetime
