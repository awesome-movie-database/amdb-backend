from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from amdb.domain.entities.review.series_episode_review import SeriesEpisodeReviewId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants import VoteType


@dataclass(slots=True)
class SeriesEpisodeReviewVote(Entity):
    series_episode_review_id: SeriesEpisodeReviewId
    user_id: UserId
    type: VoteType
