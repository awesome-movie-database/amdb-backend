from dataclasses import dataclass

from amdb.domain.entities.base import Entity
from amdb.domain.entities.review.movie_review import MovieReviewId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants import VoteType


@dataclass(slots=True)
class MovieReviewType(Entity):
    movie_review_id: MovieReviewId
    user_id: UserId
    type: VoteType
