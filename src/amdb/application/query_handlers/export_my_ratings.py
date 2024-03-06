from amdb.application.common.entities.file import File
from amdb.application.common.services.convert_to_file import (
    ConvertMyRatingsToFile,
)
from amdb.application.common.readers.rating_for_export import (
    RatingForExportViewModelsReader,
)
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.queries.export_my_ratings import ExportMyRatingsQuery


class ExportMyRatingsHandler:
    def __init__(
        self,
        *,
        convert_my_ratings_to_file: ConvertMyRatingsToFile,
        ratings_for_export_reader: RatingForExportViewModelsReader,
        identity_provider: IdentityProvider,
    ) -> None:
        self._convert_my_ratings_to_file = convert_my_ratings_to_file
        self._ratings_for_export_reader = ratings_for_export_reader
        self._identity_provider = identity_provider

    def execute(self, query: ExportMyRatingsQuery) -> File:
        current_user_id = self._identity_provider.user_id()

        view_models = self._ratings_for_export_reader.get(
            current_user_id=current_user_id,
        )
        file = self._convert_my_ratings_to_file(
            view_models=view_models,
            format=query.format,
        )

        return file
