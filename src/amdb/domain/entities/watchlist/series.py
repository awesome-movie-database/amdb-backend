from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.watchlist.watchlist import WatchlistId
from amdb.domain.entities.series.series import SeriesId


@dataclass(slots=True)
class WatchlistSeries(Entity):
    watchlist_id: WatchlistId
    series_id: SeriesId
    created_at: datetime
