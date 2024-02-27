from amdb.application.common.constants.export import ExportFormat
from amdb.application.common.readers.rating_for_export import (
    RatingForExportViewModelsReader,
)
from amdb.application.common.converters.rating_for_export import (
    RatingsForExportConverter,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.common.view_models.rating_for_export import (
    RatingForExportViewModel,
)
from amdb.application.queries.export_my_ratings import ExportMyRatingsQuery


class ExportMyRatingsHandler:
    def __init__(
        self,
        *,
        ratings_for_export_reader: RatingForExportViewModelsReader,
        ratings_for_export_converter: RatingsForExportConverter,
        identity_provider: IdentityProvider,
    ) -> None:
        self._ratings_for_export_reader = ratings_for_export_reader
        self._ratings_for_export_converter = ratings_for_export_converter
        self._identity_provider = identity_provider

    def execute(self, query: ExportMyRatingsQuery) -> str:
        current_user_id = self._identity_provider.user_id()

        view_models = self._ratings_for_export_reader.get(
            current_user_id=current_user_id,
        )
        return self._convert_view_models_to_format(
            view_models=view_models,
            format=query.format,
        )

    def _convert_view_models_to_format(
        self,
        view_models: list[RatingForExportViewModel],
        format: ExportFormat,
    ) -> str:
        if format is ExportFormat.CSV:
            return self._ratings_for_export_converter.to_csv(view_models)
