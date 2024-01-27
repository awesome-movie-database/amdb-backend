from dataclasses import dataclass
from datetime import datetime

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, ReviewType


@dataclass(frozen=True, slots=True)
class GetMovieReviewsQuery:
    movie_id: MovieId
    limit: int
    offset: int


@dataclass(frozen=True, slots=True)
class Review:
    id: ReviewId
    user_id: UserId
    movie_id: MovieId
    title: str
    content: str
    type: ReviewType
    created_at: datetime


@dataclass(frozen=True, slots=True)
class GetMovieReviewsResult:
    reviews: list[Review]
    review_count: int
