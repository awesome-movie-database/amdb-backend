from datetime import date
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId


class UserRating(TypedDict):
    id: RatingId
    value: float


class NonDetailedMovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    user_rating: Optional[UserRating]
