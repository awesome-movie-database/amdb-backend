from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie


class RemoveVotesFromMovie(Service):

    def __call__(
        self,
        movie: Movie,
        *votes: float,
    ) -> None:
        if movie.amdb_vote_count == 1:
            movie.amdb_rating = None
            movie.amdb_vote_count = 0
            return

        movie.amdb_rating = (
            ((movie.amdb_rating * movie.amdb_vote_count) - sum(votes))  # type: ignore
            / (movie.amdb_vote_count - len(votes))
        )
        movie.amdb_vote_count -= len(votes)