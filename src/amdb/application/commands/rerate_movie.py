from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class RerateMovieCommand:
    movie_id: MovieId
    new_rating: float
