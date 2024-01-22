from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetMoviesQuery:
    limit: int
    offset: int


@dataclass(frozen=True, slots=True)
class Movie:
    id: MovieId
    title: str
    rating: float
    rating_count: int


@dataclass(frozen=True, slots=True)
class GetMoviesResult:
    movies: list[Movie]
    movie_count: int
