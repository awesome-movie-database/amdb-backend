from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants.common import ReviewType


SeriesReviewId = NewType("SeriesReviewId", UUID)


@dataclass(slots=True)
class SeriesReview(Entity):
    id: SeriesReviewId
    series_id: SeriesId
    user_id: UserId
    type: ReviewType
    title: str
    content: str
    likes: int
    dislikes: int
    is_approved: bool
    created_at: datetime
