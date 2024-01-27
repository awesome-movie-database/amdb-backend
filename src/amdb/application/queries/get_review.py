from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, ReviewType


@dataclass(frozen=True, slots=True)
class GetReviewQuery:
    review_id: ReviewId


@dataclass(frozen=True, slots=True)
class GetReviewResult:
    user_id: UserId
    movie_id: MovieId
    title: str
    content: str
    type: ReviewType
    created_at: datetime
