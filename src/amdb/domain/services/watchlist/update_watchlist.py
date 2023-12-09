from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.watchlist.watchlist import Watchlist


class UpdateWatchlist(Service):
    def __call__(
        self,
        *,
        watchlist: Watchlist,
        is_private: bool,
        timestamp: datetime,
    ) -> None:
        watchlist.is_private = is_private
        watchlist.updated_at = timestamp
