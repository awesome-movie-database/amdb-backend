from datetime import datetime
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.user import UserId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType


class RatingViewModel(TypedDict):
    id: RatingId
    value: float
    created_at: datetime


class ReviewViewModel(TypedDict):
    id: ReviewId
    title: str
    content: str
    type: ReviewType
    created_at: datetime


class DetailedReviewViewModel(TypedDict):
    user_id: UserId
    review: ReviewViewModel
    rating: Optional[RatingViewModel]
