from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.exceptions.series_episode import SeriesEpisodeNotUnderInspection


class RemoveSeriesEpisodeFromInspection(Service):

    def __call__(
        self,
        series: Series,
    ) -> None:
        if not series.is_under_inspection:
            raise SeriesEpisodeNotUnderInspection()
        series.is_under_inspection = False
