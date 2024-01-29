from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId


@dataclass(frozen=True, slots=True)
class GetMyRatingsQuery:
    limit: int
    offset: int


@dataclass(frozen=True, slots=True)
class Rating:
    id: RatingId
    user_id: UserId
    movie_id: MovieId
    value: float
    created_at: datetime


@dataclass(frozen=True, slots=True)
class GetMyRatingsResult:
    ratings: list[Rating]
    rating_count: int
