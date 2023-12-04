from datetime import datetime
from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.movie_review import MovieReview
from amdb.domain.constants import ReviewType


class ReviewMovie(Service):
    @overload
    def __init__(
        self,
        *,
        auto_approve: Literal[True],
        approved_reviews_for_auto_approve: int,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        *,
        auto_approve: Literal[False],
        approved_reviews_for_auto_approve: None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        auto_approve: bool,
        approved_reviews_for_auto_approve: Optional[int],
    ) -> None:
        self._auto_approve = auto_approve
        self._approved_reviews_for_auto_approve = approved_reviews_for_auto_approve

    def __call__(
        self,
        *,
        movie: Movie,
        profile: Profile,
        type: ReviewType,
        title: str,
        content: str,
        likes: int,
        dislikes: int,
        created_at: datetime,
    ) -> MovieReview:
        profile.movie_reviews += 1

        if self._auto_approve and self._approved_reviews_for_auto_approve <= profile.movie_reviews:
            profile.approved_reviews += 1

            return MovieReview(
                movie_id=movie.id,
                user_id=profile.user_id,
                type=type,
                title=title,
                content=content,
                likes=likes,
                dislikes=dislikes,
                is_approved=True,
                created_at=created_at,
            )

        return MovieReview(
            movie_id=movie.id,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=likes,
            dislikes=dislikes,
            is_approved=False,
            created_at=created_at,
        )
