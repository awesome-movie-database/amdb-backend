from datetime import datetime

from amdb.domain.entities.user import User
from amdb.domain.entities.movie import Movie
from amdb.domain.entities.rating import Rating


class RateMovie:
    def __call__(
        self,
        *,
        user: User,
        movie: Movie,
        rating: float,
        current_timestamp: datetime,
    ) -> Rating:
        movie.rating = (movie.rating * movie.rating_count + rating) / (
            movie.rating_count + 1
        )
        movie.rating_count += 1

        return Rating(
            movie_id=movie.id,
            user_id=user.id,
            rating=rating,
            created_at=current_timestamp,
        )
