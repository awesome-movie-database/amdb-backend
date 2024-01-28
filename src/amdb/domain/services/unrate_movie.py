from amdb.domain.entities.movie import Movie
from amdb.domain.entities.rating import Rating


class UnrateMovie:
    def __call__(
        self,
        *,
        movie: Movie,
        rating: Rating,
    ) -> None:
        if movie.rating_count == 1:
            movie.rating = 0
            movie.rating_count = 0
        else:
            movie.rating = (movie.rating * movie.rating_count - rating.value) / (
                movie.rating_count - 1
            )
            movie.rating_count -= 1
