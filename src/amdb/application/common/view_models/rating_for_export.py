from datetime import date, datetime

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId


class MovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int


class RatingViewModel(TypedDict):
    value: float
    created_at: datetime


class RatingForExportViewModel(TypedDict):
    movie: MovieViewModel
    rating: RatingViewModel
