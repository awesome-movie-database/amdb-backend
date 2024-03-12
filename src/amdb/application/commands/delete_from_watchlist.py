from dataclasses import dataclass

from amdb.domain.entities.movie_for_later import MovieForLaterId


@dataclass(frozen=True, slots=True)
class DeleteFromWatchlistCommand:
    movie_for_later_id: MovieForLaterId
