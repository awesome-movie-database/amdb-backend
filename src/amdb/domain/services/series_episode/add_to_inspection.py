from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode.episode import SeriesEpisode
from amdb.domain.exceptions.series_episode import SeriesEpisodeUnderInspection


class AddSeriesEpisodeToInspection(Service):

    def __call__(
        self,
        series_episode: SeriesEpisode,
    ) -> None:
        if series_episode.is_under_inspection:
            raise SeriesEpisodeUnderInspection()
        series_episode.is_under_inspection = True
