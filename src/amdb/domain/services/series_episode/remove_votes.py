from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode.episode import SeriesEpisode


class RemoveVotesFromSeriesEpisode(Service):

    def __call__(
        self,
        series_episode: SeriesEpisode,
        *votes: float,
    ) -> None:
        if series_episode.amdb_vote_count == 1:
            series_episode.amdb_rating = None
            series_episode.amdb_vote_count = 0
            return

        series_episode.amdb_rating = (
            ((series_episode.amdb_rating * series_episode.amdb_vote_count) - sum(votes))  # type: ignore
            / (series_episode.amdb_vote_count - len(votes))
        )
        series_episode.amdb_vote_count -= len(votes)
