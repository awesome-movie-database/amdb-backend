from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series


class AddVotesToSeries(Service):
    
    def __call__(
        self,
        series: Series,
        *votes: float,
    ) -> None:
        if series.amdb_rating is None:
            series.amdb_rating = sum(votes) / len(votes)
            series.amdb_vote_count = len(votes)
            return

        series.amdb_rating = (
            ((series.amdb_rating * series.amdb_vote_count) + sum(votes))
            / (series.amdb_vote_count + len(votes))
        )
        series.amdb_vote_count += len(votes)
