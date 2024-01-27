from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetMovieRatingsQuery:
    movie_id: MovieId
    limit: int
    offset: int


@dataclass(frozen=True, slots=True)
class Rating:
    user_id: UserId
    movie_id: MovieId
    value: float
    created_at: datetime


@dataclass(frozen=True, slots=True)
class GetMovieRatingsResult:
    ratings: list[Rating]
    rating_count: int
