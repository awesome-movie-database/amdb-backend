from amdb.application.common.view_models.my_detailed_ratings import (
    MyDetailedRatingsViewModel,
)
from amdb.application.common.readers.my_detailed_ratings import (
    MyDetailedRatingsViewModelReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.queries.my_detailed_ratings import (
    GetMyDetailedRatingsQuery,
)


class GetMyDetailedRatingsQueryHandler:
    def __init__(
        self,
        *,
        my_detailed_ratings_reader: MyDetailedRatingsViewModelReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._my_detailed_ratings_reader = my_detailed_ratings_reader
        self._identity_provider = identity_provider

    def execute(
        self,
        query: GetMyDetailedRatingsQuery,
    ) -> MyDetailedRatingsViewModel:
        current_user_id = self._identity_provider.user_id()

        view_model = self._my_detailed_ratings_reader.get(
            current_user_id=current_user_id,
            limit=query.limit,
            offset=query.offset,
        )

        return view_model
