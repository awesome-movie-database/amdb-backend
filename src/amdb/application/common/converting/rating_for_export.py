from typing import Protocol

from amdb.application.common.entities.file import File
from amdb.application.common.view_models.rating_for_export import (
    RatingForExportViewModel,
)


class RatingsForExportConverter(Protocol):
    def to_csv(
        self,
        view_models: list[RatingForExportViewModel],
    ) -> File:
        raise NotImplementedError
