from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_episode_review import (
    SeriesEpisodeReviewId,
    SeriesEpisodeReview,
)
from amdb.domain.constants.common import ReviewType


class ReviewSeriesEpisode(Service):
    def __call__(
        self,
        *,
        episode: SeriesEpisode,
        profile: Profile,
        id: SeriesEpisodeReviewId,
        type: ReviewType,
        title: str,
        content: str,
        is_approved: bool,
        timestamp: datetime,
    ) -> SeriesEpisodeReview:
        profile.series_episode_reviews += 1

        if is_approved:
            profile.approved_reviews += 1

        return SeriesEpisodeReview(
            id=id,
            series_id=episode.series_id,
            season_number=episode.season_number,
            episode_number=episode.number,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=0,
            dislikes=0,
            is_approved=is_approved,
            created_at=timestamp,
        )
