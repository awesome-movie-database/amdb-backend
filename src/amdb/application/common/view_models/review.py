from datetime import datetime
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.user import UserId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType


class UserRating(TypedDict):
    id: RatingId
    value: float
    created_at: datetime


class UserReview(TypedDict):
    id: ReviewId
    title: str
    content: str
    type: ReviewType
    created_at: datetime


class ReviewViewModel(TypedDict):
    user_id: UserId
    user_review: UserReview
    user_rating: Optional[UserRating]
