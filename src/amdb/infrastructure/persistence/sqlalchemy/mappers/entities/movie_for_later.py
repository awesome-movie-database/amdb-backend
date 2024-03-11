from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert, and_

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.movie_for_later import MovieForLater, MovieForLaterId
from amdb.infrastructure.persistence.sqlalchemy.models.movie_for_later import (
    MovieForLaterModel,
)


class MovieForLaterMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[MovieForLater]:
        statement = select(MovieForLaterModel).where(
            and_(
                MovieForLaterModel.user_id == user_id,
                MovieForLaterModel.movie_id == movie_id,
            ),
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)
        return None

    def save(self, movie_for_later: MovieForLater) -> None:
        statement = insert(MovieForLaterModel).values(
            id=movie_for_later.id,
            user_id=movie_for_later.user_id,
            movie_id=movie_for_later.movie_id,
            note=movie_for_later.note,
            created_at=movie_for_later.created_at,
        )
        self._connection.execute(statement)

    def _to_entity(
        self,
        row: Annotated[MovieForLaterModel, Row],
    ) -> MovieForLater:
        return MovieForLater(
            id=MovieForLaterId(row.id),
            user_id=UserId(row.user_id),
            movie_id=MovieId(row.movie_id),
            note=row.note,
            created_at=row.created_at,
        )
