from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from .movie import MovieId
from .user import UserId


RatingId = NewType("RatingId", UUID)


@dataclass(slots=True)
class Rating:
    id: RatingId
    movie_id: MovieId
    user_id: UserId
    value: float
    created_at: datetime
