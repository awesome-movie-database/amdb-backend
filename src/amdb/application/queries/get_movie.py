from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetMovieQuery:
    movie_id: MovieId


@dataclass(frozen=True, slots=True)
class GetMovieResult:
    title: str
    rating: float
    rating_count: int
