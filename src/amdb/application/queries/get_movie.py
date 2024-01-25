from dataclasses import dataclass
from datetime import date

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetMovieQuery:
    movie_id: MovieId


@dataclass(frozen=True, slots=True)
class GetMovieResult:
    title: str
    release_date: date
    rating: float
    rating_count: int
