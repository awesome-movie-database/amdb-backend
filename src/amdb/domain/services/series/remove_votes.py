from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series


class RemoveVotesFromSeries(Service):

    def __call__(
        self,
        series: Series,
        *votes: float,
    ) -> None:
        if series.amdb_vote_count == 1:
            series.amdb_rating = None
            series.amdb_vote_count = 0
            return

        series.amdb_rating = (
            ((series.amdb_rating * series.amdb_vote_count) - sum(votes))  # type: ignore
            / (series.amdb_vote_count - len(votes))
        )
        series.amdb_vote_count -= len(votes)
