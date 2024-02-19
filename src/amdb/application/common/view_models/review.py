__all__ = ("ReviewViewModel",)

from datetime import datetime
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType


class Rating(TypedDict):
    id: RatingId
    value: float
    created_at: datetime


class Review(TypedDict):
    id: ReviewId
    title: str
    content: str
    type: ReviewType
    created_at: datetime


class ReviewViewModel(TypedDict):
    user_id: UserId
    movie_id: MovieId
    review: Review
    rating: Optional[Rating]
