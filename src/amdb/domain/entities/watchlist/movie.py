from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from .watchlist import WatchlistId


@dataclass(slots=True)
class WatchlistMovie(Entity):
    watchlist_id: WatchlistId
    movie_id: MovieId
    created_at: datetime
