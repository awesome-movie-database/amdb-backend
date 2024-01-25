from datetime import datetime

from amdb.domain.entities.user import User
from amdb.domain.entities.movie import Movie
from amdb.domain.entities.review import ReviewId, ReviewType, Review


class ReviewMovie:
    def __call__(
        self,
        *,
        id: ReviewId,
        user: User,
        movie: Movie,
        title: str,
        content: str,
        type: ReviewType,
        current_timestamp: datetime,
    ) -> Review:
        return Review(
            id=id,
            user_id=user.id,
            movie_id=movie.id,
            title=title,
            content=content,
            type=type,
            created_at=current_timestamp,
        )
