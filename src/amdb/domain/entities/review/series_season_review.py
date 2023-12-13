from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants.common import ReviewType


SeriesSeasonReviewId = NewType("SeriesSeasonReviewId", UUID)


@dataclass(slots=True)
class SeriesSeasonReview(Entity):
    id: SeriesSeasonReviewId
    series_id: SeriesId
    season_number: int
    user_id: UserId
    type: ReviewType
    title: str
    content: str
    likes: int
    dislikes: int
    is_approved: bool
    created_at: datetime
