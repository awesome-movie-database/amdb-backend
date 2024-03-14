from datetime import date, datetime

from typing_extensions import TypedDict

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.movie_for_later import MovieForLaterId


class MovieViewModel(TypedDict):
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int


class MovieForLaterViewModel(TypedDict):
    id: MovieForLaterId
    note: str
    created_at: datetime


class DetailedMovieForLaterViewModel(TypedDict):
    movie: MovieViewModel
    movie_for_later: MovieForLaterViewModel


class MyDetailedWatchlistViewModel(TypedDict):
    detailed_movies_for_later: list[DetailedMovieForLaterViewModel]
    movie_for_later_count: int
