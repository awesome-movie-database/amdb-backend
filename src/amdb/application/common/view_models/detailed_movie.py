from datetime import date, datetime
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType


class UserRatingViewModel(TypedDict):
    id: RatingId
    value: float
    created_at: datetime


class UserReviewViewModel(TypedDict):
    id: ReviewId
    title: str
    content: str
    type: ReviewType
    created_at: datetime


class MovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int


class DetailedMovieViewModel(TypedDict):
    movie: MovieViewModel
    user_rating: Optional[UserRatingViewModel]
    user_review: Optional[UserReviewViewModel]
