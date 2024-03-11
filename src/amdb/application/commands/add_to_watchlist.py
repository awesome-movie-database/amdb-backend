from dataclasses import dataclass

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class AddToWatchlistCommand:
    movie_id: MovieId
    note: str
