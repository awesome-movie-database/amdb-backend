from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from enum import IntEnum
from uuid import UUID

from .user import UserId
from .movie import MovieId


ReviewId = NewType("ReviewId", UUID)


class ReviewType(IntEnum):
    NEUTRAL = 0
    POSITIVE = 1
    NEGATIVE = 2


@dataclass(frozen=True, slots=True)
class Review:
    id: ReviewId
    user_id: UserId
    movie_id: MovieId
    title: str
    content: str
    type: ReviewType
    created_at: datetime
