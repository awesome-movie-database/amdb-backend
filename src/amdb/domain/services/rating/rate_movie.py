from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.user.user import User
from amdb.domain.entities.rating.movie_rating import MovieRating
from amdb.domain.value_objects import Rating


class RateMovie(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        user: User,
        rating: Rating,
        created_at: datetime,
    ) -> MovieRating:
        self._add_rating_to_movie(
            movie=movie,
            rating=rating,
        )

        return MovieRating(
            movie_id=movie.id,
            user_id=user.id,
            rating=rating,
            created_at=created_at,
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
