from typing import Protocol

from amdb.domain.entities.user import UserId
from amdb.application.common.view_models.my_detailed_ratings import (
    MyDetailedRatingsViewModel,
)


class MyDetailedRatingsViewModelReader(Protocol):
    def get(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> MyDetailedRatingsViewModel:
        raise NotImplementedError
