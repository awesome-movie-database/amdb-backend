from typing import Protocol

from amdb.domain.entities.user import UserId
from amdb.application.common.view_models.rating_for_export import (
    RatingForExportViewModel,
)


class RatingForExportViewModelsReader(Protocol):
    def get(
        self,
        current_user_id: UserId,
    ) -> list[RatingForExportViewModel]:
        raise NotImplementedError
