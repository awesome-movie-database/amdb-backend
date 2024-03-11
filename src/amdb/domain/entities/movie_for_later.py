from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from .user import UserId
from .movie import MovieId


MovieForLaterId = NewType("MovieForLaterId", UUID)


@dataclass(slots=True)
class MovieForLater:
    id: MovieForLaterId
    user_id: UserId
    movie_id: MovieId
    note: str
    created_at: datetime
