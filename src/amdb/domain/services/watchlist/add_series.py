from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.watchlist.watchlist import Watchlist
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.watchlist.series import WatchlistSeries


class AddSeriesToWatchlist(Service):
    def __call__(
        self,
        *,
        watchlist: Watchlist,
        series: Series,
        timestamp: datetime,
    ) -> WatchlistSeries:
        watchlist.updated_at = timestamp

        return WatchlistSeries(
            watchlist_id=watchlist.id,
            series_id=series.id,
            created_at=timestamp,
        )
