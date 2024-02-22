__all__ = ("DetailedMovieViewModelMapper",)

from typing import Optional, TypedDict
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Connection, Row, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType
from amdb.application.common.view_models.detailed_movie import (
    UserRating,
    UserReview,
    DetailedMovieViewModel,
)


class RowAsDict(TypedDict):
    movie_id: UUID
    movie_title: str
    movie_release_date: date
    movie_rating: float
    movie_rating_count: int
    user_rating_id: Optional[UUID]
    user_rating_value: Optional[float]
    user_rating_created_at: Optional[datetime]
    user_review_id: Optional[UUID]
    user_review_title: Optional[str]
    user_review_content: Optional[str]
    user_review_type: Optional[int]
    user_review_created_at: Optional[datetime]

    @classmethod  # type: ignore
    def from_row(cls, row: Row) -> "RowAsDict":
        return RowAsDict(**row._mapping)  # noqa: SLF001


class DetailedMovieViewModelMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def one(
        self,
        movie_id: MovieId,
        current_user_id: Optional[UserId],
    ) -> Optional[DetailedMovieViewModel]:
        statement = text(
            """
            SELECT
                m.id movie_id,
                m.title movie_title,
                m.release_date movie_release_date,
                m.rating movie_rating,
                m.rating_count movie_rating_count,
                urt.id user_rating_id,
                urt.value user_rating_value,
                urt.created_at user_rating_created_at,
                urv.id user_review_id,
                urv.title user_review_title,
                urv.content user_review_content,
                urv.type user_review_type,
                urv.created_at user_review_created_at
            FROM
                movies m
            LEFT JOIN ratings urt
                ON urt.user_id = :current_user_id
            LEFT JOIN reviews urv
                ON urv.user_id = :current_user_id
            WHERE
                m.id = :movie_id
            LIMIT 1
            """,
        )
        parameters = {
            "movie_id": movie_id,
            "current_user_id": current_user_id,
        }
        row = self._connection.execute(statement, parameters).fetchone()
        if row:
            row_as_dict = RowAsDict.from_row(row)  # type: ignore
            return self._to_view_model(row_as_dict)
        return None

    def _to_view_model(
        self,
        row_as_dict: RowAsDict,
    ) -> DetailedMovieViewModel:
        if row_as_dict["user_rating_id"]:
            user_rating = UserRating(
                id=RatingId(row_as_dict["user_rating_id"]),  # type: ignore
                value=row_as_dict["user_rating_value"],  # type: ignore
                created_at=row_as_dict["user_rating_created_at"],  # type: ignore
            )
        else:
            user_rating = None

        if row_as_dict["user_review_id"]:
            user_review = UserReview(
                id=ReviewId(row_as_dict["user_review_id"]),  # type: ignore
                title=row_as_dict["user_review_title"],  # type: ignore
                content=row_as_dict["user_review_content"],  # type: ignore
                type=ReviewType(row_as_dict["user_review_type"]),  # type: ignore
                created_at=row_as_dict["user_review_created_at"],  # type: ignore
            )
        else:
            user_review = None

        detailed_movie_view_model = DetailedMovieViewModel(
            id=MovieId(row_as_dict["movie_id"]),
            title=row_as_dict["movie_title"],
            release_date=row_as_dict["movie_release_date"],
            rating=row_as_dict["movie_rating"],
            rating_count=row_as_dict["movie_rating_count"],
            user_rating=user_rating,
            user_review=user_review,
        )
        return detailed_movie_view_model
