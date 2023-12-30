from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class RateMovieCommand:
    movie_id: MovieId
    rating: float
