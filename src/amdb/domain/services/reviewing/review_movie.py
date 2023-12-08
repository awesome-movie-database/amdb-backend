from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.movie_review import MovieReviewId, MovieReview
from amdb.domain.constants import ReviewType


class ReviewMovie(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        profile: Profile,
        id: MovieReviewId,
        type: ReviewType,
        title: str,
        content: str,
        is_approved: bool,
        created_at: datetime,
    ) -> MovieReview:
        profile.movie_reviews += 1

        if is_approved:
            profile.approved_reviews += 1

        return MovieReview(
            id=id,
            movie_id=movie.id,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=0,
            dislikes=0,
            is_approved=is_approved,
            created_at=created_at,
        )
