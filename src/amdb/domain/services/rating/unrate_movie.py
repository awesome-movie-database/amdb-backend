from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.rating.movie_rating import MovieRating
from amdb.domain.value_objects import Rating


class UnrateMovie(Service):
    def __call__(
        self,
        movie_rating: MovieRating,
        movie: Movie,
    ) -> None:
        self._remove_rating_from_movie(
            movie=movie,
            rating=movie_rating.rating,
        )

    def _remove_rating_from_movie(
        self,
        movie: Movie,
        rating: Rating,
    ) -> None:
        movie.rating = (movie.rating * movie.rating_count - rating.value) / (
            movie.rating_count - 1
        )
        movie.rating_count -= 1
