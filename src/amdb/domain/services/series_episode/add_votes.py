from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode.episode import SeriesEpisode


class AddVotesToSeriesEpisode(Service):
    
    def __call__(
        self,
        series_episode: SeriesEpisode,
        *votes: float,
    ) -> None:
        if series_episode.amdb_rating is None:
            series_episode.amdb_rating = sum(votes) / len(votes)
            series_episode.amdb_vote_count = len(votes)
            return

        series_episode.amdb_rating = (
            ((series_episode.amdb_rating * series_episode.amdb_vote_count) + sum(votes))
            / (series_episode.amdb_vote_count + len(votes))
        )
        series_episode.amdb_vote_count += len(votes)
