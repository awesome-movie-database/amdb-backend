from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.rating.movie_rating import MovieRating, UncountedMovieRating
from amdb.domain.value_objects import Rating


class CountMovieRating(Service):
    def __call__(
        self,
        uncounted_movie_rating: UncountedMovieRating,
        movie: Movie,
    ) -> MovieRating:
        self._add_rating_to_movie(
            movie=movie,
            rating=uncounted_movie_rating.rating,
        )

        return MovieRating(
            movie_id=uncounted_movie_rating.movie_id,
            user_id=uncounted_movie_rating.user_id,
            rating=uncounted_movie_rating.rating,
            created_at=uncounted_movie_rating.created_at,
        )

    def _add_rating_to_movie(
        self,
        movie: Movie,
        rating: Rating,
    ) -> None:
        movie.rating = (movie.rating * movie.rating_count + rating.value) / (
            movie.rating_count + 1
        )
        movie.rating_count += 1
