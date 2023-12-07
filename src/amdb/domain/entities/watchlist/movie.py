from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.watchlist.watchlist import WatchlistId
from amdb.domain.entities.movie.movie import MovieId


@dataclass(slots=True)
class WatchlistMovie(Entity):
    watchlist_id: WatchlistId
    movie_id: MovieId
    created_at: datetime
