from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.watchlist.watchlist import WatchlistId, Watchlist


class CreateWatchlist(Service):
    def __call__(
        self,
        *,
        profile: Profile,
        id: WatchlistId,
        created_at: datetime,
    ) -> Watchlist:
        return Watchlist(
            id=id,
            user_id=profile.user_id,
            is_private=True,
            created_at=created_at,
            updated_at=None,
        )
