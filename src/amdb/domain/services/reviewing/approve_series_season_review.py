from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_season_review import SeriesSeasonReview


class ApproveSeriesSeasonReview(Service):
    @overload
    def __call__(
        self,
        *,
        series_season_review: SeriesSeasonReview,
        is_approved: Literal[True],
        profile: Profile,
    ) -> None:
        ...

    @overload
    def __call__(
        self,
        *,
        series_season_review: SeriesSeasonReview,
        is_approved: Literal[False],
    ) -> None:
        ...

    def __call__(
        self,
        *,
        series_season_review: SeriesSeasonReview,
        is_approved: bool,
        profile: Optional[Profile] = None,
    ) -> None:
        if is_approved:
            profile.approved_reviews += 1  # type: ignore
        series_season_review.is_approved = is_approved
