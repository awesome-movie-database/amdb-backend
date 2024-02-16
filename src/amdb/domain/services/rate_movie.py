from datetime import datetime

from amdb.domain.entities.user import User
from amdb.domain.entities.movie import Movie
from amdb.domain.entities.rating import RatingId, Rating
from amdb.domain.constants.exceptions import INVALID_RATING_VALUE
from amdb.domain.exception import DomainError


class RateMovie:
    def __call__(
        self,
        *,
        id: RatingId,
        user: User,
        movie: Movie,
        rating: float,
        current_timestamp: datetime,
    ) -> Rating:
        if rating <= 0 or rating > 10 or rating % 0.5 != 0:
            raise DomainError(INVALID_RATING_VALUE)

        movie.rating = (movie.rating * movie.rating_count + rating) / (
            movie.rating_count + 1
        )
        movie.rating_count += 1

        return Rating(
            id=id,
            movie_id=movie.id,
            user_id=user.id,
            value=rating,
            created_at=current_timestamp,
        )
