from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.base import Entity
from amdb.domain.entities.series.series import SeriesId
from .watchlist import WatchlistId


@dataclass(slots=True)
class WatchlistSeries(Entity):
    watchlist_id: WatchlistId
    series_id: SeriesId
    created_at: datetime
