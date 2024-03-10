from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert, delete, and_

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.infrastructure.persistence.sqlalchemy.models.review import (
    ReviewModel,
)


class ReviewMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_id(self, review_id: ReviewId) -> Optional[Review]:
        statement = select(ReviewModel).where(ReviewModel.id == review_id)
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[Review]:
        statement = select(ReviewModel).where(
            and_(
                ReviewModel.user_id == user_id,
                ReviewModel.movie_id == movie_id,
            ),
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def save(self, review: Review) -> None:
        statement = insert(ReviewModel).values(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            title=review.title,
            content=review.content,
            type=review.type.value,
            created_at=review.created_at,
        )
        self._connection.execute(statement)

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        statement = delete(ReviewModel).where(ReviewModel.movie_id == movie_id)
        self._connection.execute(statement)

    def _to_entity(
        self,
        row: Annotated[ReviewModel, Row],
    ) -> Review:
        return Review(
            id=ReviewId(row.id),
            user_id=UserId(row.user_id),
            movie_id=MovieId(row.movie_id),
            title=row.title,
            content=row.content,
            type=ReviewType(row.type),
            created_at=row.created_at,
        )
