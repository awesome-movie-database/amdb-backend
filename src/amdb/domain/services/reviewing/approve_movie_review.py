from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.movie_review import MovieReview


class ApproveSeriesReview(Service):
    @overload
    def __call__(
        self,
        *,
        movie_review: MovieReview,
        is_approved: Literal[True],
        profile: Profile,
    ) -> None:
        ...

    @overload
    def __call__(
        self,
        *,
        movie_review: MovieReview,
        is_approved: Literal[False],
    ) -> None:
        ...

    def __call__(
        self,
        *,
        movie_review: MovieReview,
        is_approved: bool,
        profile: Optional[Profile] = None,
    ) -> None:
        if is_approved:
            profile.approved_reviews += 1  # type: ignore
        movie_review.is_approved = is_approved
