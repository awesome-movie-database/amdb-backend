__all__ = ("DetailedReviewViewModelMapper",)

from typing import Optional, TypedDict
from datetime import datetime
from uuid import UUID

from sqlalchemy import Connection, Row, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType
from amdb.application.common.view_models.detailed_review import (
    UserRating,
    UserReview,
    DetailedReviewViewModel,
)


class RowAsDict(TypedDict):
    user_id: UUID
    user_review_id: UUID
    user_review_title: str
    user_review_content: str
    user_review_type: int
    user_review_created_at: datetime
    user_rating_id: Optional[UUID]
    user_rating_value: Optional[float]
    user_rating_created_at: Optional[datetime]

    @classmethod  # type: ignore
    def from_row(cls, row: Row) -> "RowAsDict":
        return RowAsDict(row._mapping)  # noqa: SLF001


class DetailedReviewViewModelMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def list(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[DetailedReviewViewModel]:
        statement = text(
            """
            SELECT
                urv.user_id user_id,
                urv.id user_review_id,
                urv.title user_review_title,
                urv.content user_review_content,
                urv.type user_review_type,
                urv.created_at user_review_created_at,
                urt.id user_rating_id,
                urt.value user_rating_value,
                urt.created_at user_rating_created_at
            FROM
                reviews urv
            LEFT JOIN ratings urt
                ON urt.movie_id = urv.movie_id
                AND urt.user_id = urv.user_id
            WHERE
                urv.movie_id = :movie_id
            LIMIT :limit OFFSET :offset
            """,
        )
        parameters = {
            "movie_id": movie_id,
            "limit": limit,
            "offset": offset,
        }
        rows = self._connection.execute(statement, parameters).fetchall()

        review_view_models = []
        for row in rows:
            row_as_dict = RowAsDict.from_row(row)  # type: ignore
            review_view_model = self._to_view_model(row_as_dict)
            review_view_models.append(review_view_model)

        return review_view_models

    def _to_view_model(
        self,
        row_as_dict: RowAsDict,
    ) -> DetailedReviewViewModel:
        user_review = UserReview(
            id=ReviewId(row_as_dict["user_review_id"]),
            title=row_as_dict["user_review_title"],
            content=row_as_dict["user_review_content"],
            type=ReviewType(row_as_dict["user_review_type"]),
            created_at=row_as_dict["user_review_created_at"],
        )

        if row_as_dict["user_rating_id"]:
            user_rating = UserRating(
                id=RatingId(row_as_dict["user_rating_id"]),  # type: ignore
                value=row_as_dict["user_rating_value"],  # type: ignore
                created_at=row_as_dict["user_rating_created_at"],  # type: ignore
            )
        else:
            user_rating = None

        detailed_review_view_model = DetailedReviewViewModel(
            user_id=UserId(row_as_dict["user_id"]),
            user_review=user_review,
            user_rating=user_rating,
        )
        return detailed_review_view_model
