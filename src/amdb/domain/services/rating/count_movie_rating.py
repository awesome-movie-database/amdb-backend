from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.rating.movie_rating import MovieRating
from amdb.domain.value_objects import Rating
from amdb.domain.exceptions.rating import MovieRatingAlreadyCountedError


class CountMovieRating(Service):
    def __call__(
        self,
        *,
        movie_rating: MovieRating,
        movie: Movie,
    ) -> None:
        if movie_rating.is_counted:
            raise MovieRatingAlreadyCountedError()

        self._add_rating_to_movie(
            movie=movie,
            rating=movie_rating.rating,
        )
        movie_rating.is_counted = True

    def _add_rating_to_movie(
        self,
        *,
        movie: Movie,
        rating: Rating,
    ) -> None:
        movie.rating = (movie.rating * movie.rating_count + rating.value) / (
            movie.rating_count + 1
        )
        movie.rating_count += 1
