from amdb.application.common.readers.my_detailed_watchlist import (
    MyDetailedWatchlistViewModelReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.my_detailed_watchlist import (
    MyDetailedWatchlistViewModel,
)
from amdb.application.queries.my_detailed_watchlist import (
    GetMyDeatiledWatchlistQuery,
)


class GetMyDetailedWatchlistHandler:
    def __init__(
        self,
        *,
        my_detailed_watchlist_reader: MyDetailedWatchlistViewModelReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._my_detailed_watchlist_reader = my_detailed_watchlist_reader
        self._identity_provider = identity_provider

    def execute(
        self,
        query: GetMyDeatiledWatchlistQuery,
    ) -> MyDetailedWatchlistViewModel:
        current_user_id = self._identity_provider.user_id()

        view_model = self._my_detailed_watchlist_reader.get(
            current_user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )

        return view_model
