from datetime import datetime
from typing import Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.user.user import User
from amdb.domain.entities.rating.movie_rating import MovieRating, UncountedMovieRating
from amdb.domain.value_objects import Rating


class RateMovie(Service):
    @overload
    def __call__(
        self,
        *,
        movie: Movie,
        user: User,
        rating: Rating,
        is_counted: Literal[True],
        created_at: datetime,
    ) -> MovieRating:
        ...

    @overload
    def __call__(
        self,
        *,
        movie: Movie,
        user: User,
        rating: Rating,
        is_counted: Literal[False],
        created_at: datetime,
    ) -> UncountedMovieRating:
        ...

    def __call__(
        self,
        *,
        movie: Movie,
        user: User,
        rating: Rating,
        is_counted: bool,
        created_at: datetime,
    ) -> MovieRating:
        if is_counted:
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

        return UncountedMovieRating(
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
