__all__ = ("NonDetailedMovieViewModelMapper",)

from typing import Optional, TypedDict
from datetime import date
from uuid import UUID

from sqlalchemy import Connection, Row, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.application.common.view_models.non_detailed_movie import (
    UserRating,
    NonDetailedMovieViewModel,
)


class RowAsDict(TypedDict):
    movie_id: UUID
    movie_title: str
    movie_release_date: date
    movie_rating: float
    user_rating_id: Optional[UUID]
    user_rating_value: Optional[float]

    @classmethod  # type: ignore
    def from_row(cls, row: Row) -> "RowAsDict":
        return RowAsDict(**row._mapping)  # noqa: SLF001


class NonDetailedMovieViewModelMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def list(
        self,
        current_user_id: Optional[UserId],
        limit: int,
        offset: int,
    ) -> list[NonDetailedMovieViewModel]:
        statement = text(
            """
            SELECT
                m.id movie_id,
                m.title movie_title,
                m.release_date movie_release_date,
                m.rating movie_rating,
                urt.id user_rating_id,
                urt.value user_rating_value
            FROM
                movies m
            LEFT JOIN ratings urt
                ON urt.user_id = :current_user_id
            LIMIT :limit OFFSET :offset
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
            "limit": limit,
            "offset": offset,
        }
        rows = self._connection.execute(statement, parameters).fetchall()

        non_detailed_view_models = []
        for row in rows:
            row_as_dict = RowAsDict.from_row(row)  # type: ignore
            non_detailed_view_model = self._to_view_model(row_as_dict)
            non_detailed_view_models.append(non_detailed_view_model)

        return non_detailed_view_models

    def _to_view_model(
        self,
        row_as_dict: RowAsDict,
    ) -> NonDetailedMovieViewModel:
        if row_as_dict["user_rating_id"]:
            user_rating = UserRating(
                id=RatingId(row_as_dict["user_rating_id"]),  # type: ignore
                value=row_as_dict["user_rating_value"],  # type: ignore
            )
        else:
            user_rating = None

        non_detailed_movie_view_model = NonDetailedMovieViewModel(
            id=MovieId(row_as_dict["movie_id"]),
            title=row_as_dict["movie_title"],
            release_date=row_as_dict["movie_release_date"],
            rating=row_as_dict["movie_rating"],
            user_rating=user_rating,
        )
        return non_detailed_movie_view_model
