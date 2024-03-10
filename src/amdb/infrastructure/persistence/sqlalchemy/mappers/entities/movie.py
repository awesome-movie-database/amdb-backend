from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert, update, delete

from amdb.domain.entities.movie import MovieId, Movie
from amdb.infrastructure.persistence.sqlalchemy.models.movie import MovieModel


class MovieMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_id(self, movie_id: MovieId) -> Optional[Movie]:
        statement = (
            select(MovieModel)
            .where(MovieModel.id == movie_id)
            .with_for_update()
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def save(self, movie: Movie) -> None:
        statement = insert(MovieModel).values(
            id=movie.id,
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            rating_count=movie.rating_count,
        )
        self._connection.execute(statement)

    def update(self, movie: Movie) -> None:
        statement = update(MovieModel).values(
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            rating_count=movie.rating_count,
        )
        self._connection.execute(statement)

    def delete(self, movie: Movie) -> None:
        statement = delete(MovieModel).where(MovieModel.id == movie.id)
        self._connection.execute(statement)

    def _to_entity(self, row: Annotated[MovieModel, Row]) -> Movie:
        return Movie(
            id=MovieId(row.id),
            title=row.title,
            release_date=row.release_date,
            rating=row.rating,
            rating_count=row.rating_count,
        )
