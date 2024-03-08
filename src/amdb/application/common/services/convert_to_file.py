from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.entities.file import File
from amdb.application.common.converting.rating_for_export import (
    RatingsForExportConverter,
)
from amdb.application.common.view_models.rating_for_export import (
    RatingForExportViewModel,
)


class ConvertMyRatingsToFile:
    def __init__(self, converter: RatingsForExportConverter) -> None:
        self._converter = converter

    def __call__(
        self,
        *,
        view_models: list[RatingForExportViewModel],
        format: ExportFormat,
    ) -> File:
        if format is ExportFormat.CSV:
            return self._converter.to_csv(view_models)
