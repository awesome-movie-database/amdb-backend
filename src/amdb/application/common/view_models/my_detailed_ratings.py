from datetime import date, datetime

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId


class MovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int


class RatingViewModel(TypedDict):
    id: RatingId
    value: float
    created_at: datetime


class DetailedRatingViewModel(TypedDict):
    movie: MovieViewModel
    rating: RatingViewModel


class MyDetailedRatingsViewModel(TypedDict):
    detailed_ratings: list[DetailedRatingViewModel]
    rating_count: int
