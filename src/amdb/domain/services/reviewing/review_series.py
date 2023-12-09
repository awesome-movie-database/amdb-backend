from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_review import SeriesReviewId, SeriesReview
from amdb.domain.constants import ReviewType


class ReviewSeries(Service):
    def __call__(
        self,
        *,
        series: Series,
        profile: Profile,
        id: SeriesReviewId,
        type: ReviewType,
        title: str,
        content: str,
        is_approved: bool,
        timestamp: datetime,
    ) -> SeriesReview:
        profile.series_reviews += 1

        if is_approved:
            profile.approved_reviews += 1

        return SeriesReview(
            id=id,
            series_id=series.id,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=0,
            dislikes=0,
            is_approved=is_approved,
            created_at=timestamp,
        )
