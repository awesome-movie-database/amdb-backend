from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie


class AddVotesToMovie(Service):
    
    def __call__(
        self,
        movie: Movie,
        *votes: float,
    ) -> None:
        if movie.amdb_rating is None:
            movie.amdb_rating = sum(votes) / len(votes)
            movie.amdb_vote_count = len(votes)
            return

        movie.amdb_rating = (
            ((movie.amdb_rating * movie.amdb_vote_count) + sum(votes))
            / (movie.amdb_vote_count + len(votes))
        )
        movie.amdb_vote_count += len(votes)
