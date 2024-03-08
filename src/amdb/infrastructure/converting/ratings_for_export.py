import csv
from io import StringIO

from amdb.application.common.entities.file import File
from amdb.application.common.view_models.rating_for_export import (
    RatingForExportViewModel,
)


class RealRatingsForExportConverter:
    def to_csv(
        self,
        view_models: list[RatingForExportViewModel],
    ) -> File:
        with StringIO() as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(
                [
                    "id",
                    "title",
                    "release_date",
                    "rating",
                    "rating_count",
                    "your_rating",
                    "your_rating_created_at",
                ],
            )
            for view_model in view_models:
                csv_writer.writerow(
                    [
                        view_model["movie"]["id"],
                        view_model["movie"]["title"],
                        view_model["movie"]["release_date"],
                        view_model["movie"]["rating"],
                        view_model["movie"]["rating_count"],
                        view_model["rating"]["value"],
                        view_model["rating"]["created_at"],
                    ],
                )
            csv_file = file.getvalue()
        return File(csv_file)
