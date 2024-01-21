from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.movie import MovieId


@dataclass(frozen=True, slots=True)
class GetRatingQuery:
    movie_id: MovieId


@dataclass(frozen=True, slots=True)
class GetRatingResult:
    value: float
    created_at: datetime
