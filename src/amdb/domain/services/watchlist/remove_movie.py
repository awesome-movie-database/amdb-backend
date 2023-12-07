from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.watchlist.watchlist import Watchlist


class RemoveMovieFromWatchlist(Service):
    def __call__(
        self,
        *,
        watchlist: Watchlist,
        updated_at: datetime,
    ) -> None:
        watchlist.updated_at = updated_at
