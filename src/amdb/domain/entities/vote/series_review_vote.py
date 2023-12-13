from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from amdb.domain.entities.review.series_review import SeriesReviewId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants.common import VoteType


@dataclass(slots=True)
class SeriesReviewVote(Entity):
    series_review_id: SeriesReviewId
    user_id: UserId
    type: VoteType
