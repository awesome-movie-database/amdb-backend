from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId


@dataclass(frozen=True, slots=True)
class GetRatingQuery:
    rating_id: RatingId


@dataclass(frozen=True, slots=True)
class GetRatingResult:
    user_id: UserId
    movie_id: MovieId
    value: float
    created_at: datetime
