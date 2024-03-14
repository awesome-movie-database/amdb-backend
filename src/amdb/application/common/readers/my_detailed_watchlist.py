from amdb.domain.entities.user import UserId
from amdb.application.common.view_models.my_detailed_watchlist import (
    MyDetailedWatchlistViewModel,
)


class MyDetailedWatchlistViewModelReader:
    def get(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> MyDetailedWatchlistViewModel:
        raise NotImplementedError
