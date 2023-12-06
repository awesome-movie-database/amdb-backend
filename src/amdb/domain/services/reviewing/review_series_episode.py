from datetime import datetime
from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.review.series_episode_review import (
    SeriesEpisodeReviewId,
    SeriesEpisodeReview,
)
from amdb.domain.constants import ReviewType


class ReviewSeriesEpisode(Service):
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
        episode: SeriesEpisode,
        profile: Profile,
        id: SeriesEpisodeReviewId,
        type: ReviewType,
        title: str,
        content: str,
        likes: int,
        dislikes: int,
        created_at: datetime,
    ) -> SeriesEpisodeReview:
        profile.series_episode_reviews += 1

        if (
            self._auto_approve
            and self._approved_reviews_for_auto_approve <= profile.series_episode_reviews  # type: ignore
        ):
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
                likes=likes,
                dislikes=dislikes,
                is_approved=True,
                created_at=created_at,
            )

        return SeriesEpisodeReview(
            id=id,
            series_id=episode.series_id,
            season_number=episode.season_number,
            episode_number=episode.number,
            user_id=profile.user_id,
            type=type,
            title=title,
            content=content,
            likes=likes,
            dislikes=dislikes,
            is_approved=False,
            created_at=created_at,
        )
