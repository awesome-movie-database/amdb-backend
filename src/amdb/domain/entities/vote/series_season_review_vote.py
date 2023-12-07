from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from amdb.domain.entities.review.series_season_review import SeriesSeasonReviewId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants import VoteType


@dataclass(slots=True)
class SeriesSeasonReviewVote(Entity):
    series_season_review_id: SeriesSeasonReviewId
    user_id: UserId
    type: VoteType
