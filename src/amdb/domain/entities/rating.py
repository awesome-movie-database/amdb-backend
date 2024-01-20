from dataclasses import dataclass
from datetime import datetime

from .movie import MovieId
from .user import UserId


@dataclass(slots=True)
class Rating:
    movie_id: MovieId
    user_id: UserId
    value: float
    created_at: datetime
