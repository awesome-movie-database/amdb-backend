from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_season_review import (
    SeriesSeasonReviewId,
    SeriesSeasonReview,
)
from amdb.domain.constants import ReviewType


class ReviewSeriesEpisode(Service):
    def __call__(
        self,
        *,
        season: SeriesSeason,
        profile: Profile,
        id: SeriesSeasonReviewId,
        type: ReviewType,
        title: str,
        content: str,
        is_approved: bool,
        created_at: datetime,
    ) -> SeriesSeasonReview:
        profile.series_season_reviews += 1

        if is_approved:
            profile.approved_reviews += 1

        return SeriesSeasonReview(
            id=id,
            series_id=season.series_id,
            season_number=season.number,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=0,
            dislikes=0,
            is_approved=is_approved,
            created_at=created_at,
        )
