from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.watchlist.watchlist import Watchlist
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.watchlist.movie import WatchlistMovie


class AddMovieToWatchlist(Service):
    def __call__(
        self,
        *,
        watchlist: Watchlist,
        movie: Movie,
        timestamp: datetime,
    ) -> WatchlistMovie:
        watchlist.updated_at = timestamp

        return WatchlistMovie(
            watchlist_id=watchlist.id,
            movie_id=movie.id,
            created_at=timestamp,
        )
