from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert, delete, and_

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId, Rating
from amdb.infrastructure.persistence.sqlalchemy.models.rating import (
    RatingModel,
)


class RatingMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_id(self, rating_id: RatingId) -> Optional[Rating]:
        statement = select(RatingModel).where(RatingModel.id == rating_id)
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def with_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[Rating]:
        statement = select(RatingModel).where(
            and_(
                RatingModel.user_id == user_id,
                RatingModel.movie_id == movie_id,
            ),
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def save(self, rating: Rating) -> None:
        statement = insert(RatingModel).values(
            id=rating.id,
            movie_id=rating.movie_id,
            user_id=rating.user_id,
            value=rating.value,
            created_at=rating.created_at,
        )
        self._connection.execute(statement)

    def delete(self, rating: Rating) -> None:
        statement = delete(RatingModel).where(RatingModel.id == rating.id)
        self._connection.execute(statement)

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        statement = delete(RatingModel).where(RatingModel.movie_id == movie_id)
        self._connection.execute(statement)

    def _to_entity(
        self,
        row: Annotated[RatingModel, Row],
    ) -> Rating:
        return Rating(
            id=RatingId(row.id),
            movie_id=MovieId(row.movie_id),
            user_id=UserId(row.user_id),
            value=row.value,
            created_at=row.created_at,
        )
