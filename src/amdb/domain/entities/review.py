from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from enum import Enum
from uuid import UUID

from .user import UserId
from .movie import MovieId


ReviewId = NewType("ReviewId", UUID)


class ReviewType(Enum):
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"


@dataclass(frozen=True, slots=True)
class Review:
    id: ReviewId
    user_id: UserId
    movie_id: MovieId
    title: str
    content: str
    type: ReviewType
    created_at: datetime
