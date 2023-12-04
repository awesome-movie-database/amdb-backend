from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.movie.movie import MovieId
from amdb.domain.entities.user.user import UserId
from amdb.domain.constants import ReviewType


MovieReviewId = NewType("MovieReviewId", UUID)


@dataclass(slots=True)
class MovieReview(Entity):
    id: MovieReviewId
    movie_id: MovieId
    user_id: UserId
    type: ReviewType
    title: str
    content: str
    likes: int
    dislikes: int
    is_approved: bool
    created_at: datetime
