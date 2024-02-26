from datetime import date
from typing import Optional

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId


class UserRatingViewModel(TypedDict):
    id: RatingId
    value: float


class MovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float


class NonDetailedMovieViewModel(TypedDict):
    movie: MovieViewModel
    user_rating: Optional[UserRatingViewModel]
