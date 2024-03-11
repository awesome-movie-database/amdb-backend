from datetime import datetime

from amdb.domain.entities.user import User
from amdb.domain.entities.movie import Movie
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.domain.constants.exceptions import (
    INVALID_REVIEW_TITLE,
    INVALID_REVIEW_CONTENT,
)
from amdb.domain.exception import DomainError


REVIEW_TITLE_MIN_LENGTH = 5
REVIEW_TITLE_MAX_LENGTH = 128
REVIEW_CONTENT_MIN_LENGTH = 5
REVIEW_CONTENT_MAX_LENGTH = 1024


class ReviewMovie:
    def __call__(
        self,
        *,
        id: ReviewId,
        user: User,
        movie: Movie,
        title: str,
        content: str,
        type: ReviewType,
        current_timestamp: datetime,
    ) -> Review:
        self._validate_title(title)
        self._validate_content(content)

        return Review(
            id=id,
            user_id=user.id,
            movie_id=movie.id,
            title=title,
            content=content,
            type=type,
            created_at=current_timestamp,
        )

    def _validate_title(self, title: str) -> None:
        title_length = len(title)
        if (
            title_length < REVIEW_TITLE_MIN_LENGTH
            or title_length > REVIEW_CONTENT_MAX_LENGTH
        ):
            raise DomainError(INVALID_REVIEW_TITLE)

    def _validate_content(self, content: str) -> None:
        content_length = len(content)
        if (
            content_length < REVIEW_CONTENT_MIN_LENGTH
            or content_length > REVIEW_CONTENT_MAX_LENGTH
        ):
            raise DomainError(INVALID_REVIEW_CONTENT)
