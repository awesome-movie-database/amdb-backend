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
        created_at: datetime,
    ) -> WatchlistSeries:
        watchlist.updated_at = created_at

        return WatchlistSeries(
            watchlist_id=watchlist.id,
            series_id=series.id,
            created_at=created_at,
        )
