from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.user.user import User
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.rating.movie_rating import MovieRating
from amdb.domain.value_objects import Rating


class RateMovie(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        user: User,
        profile: Profile,
        rating: Rating,
        is_counted: bool,
        created_at: datetime,
    ) -> MovieRating:
        profile.movie_ratings += 1

        if is_counted:
            self._add_rating_to_movie(
                movie=movie,
                rating=rating,
            )

        return MovieRating(
            movie_id=movie.id,
            user_id=user.id,
            rating=rating,
            is_counted=is_counted,
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
