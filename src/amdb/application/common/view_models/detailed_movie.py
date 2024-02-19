from datetime import date, datetime
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
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


class DetailedMovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int
    user_rating: Optional[UserRating]
    user_review: Optional[UserReview]
