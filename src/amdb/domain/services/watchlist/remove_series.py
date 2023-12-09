from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.watchlist.watchlist import Watchlist


class RemoveSeriesFromWatchlist(Service):
    def __call__(
        self,
        *,
        watchlist: Watchlist,
        timestamp: datetime,
    ) -> None:
        watchlist.updated_at = timestamp
