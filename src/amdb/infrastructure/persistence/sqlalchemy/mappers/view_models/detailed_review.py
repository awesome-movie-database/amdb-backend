from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType
from amdb.application.common.view_models.detailed_review import (
    RatingViewModel,
    ReviewViewModel,
    DetailedReviewViewModel,
)


class DetailedReviewViewModelsMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def get(
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

        view_models = []
        for row in rows:
            row_as_dict = row._mapping  # noqa: SLF001

            review = ReviewViewModel(
                id=ReviewId(row_as_dict["user_review_id"]),
                title=row_as_dict["user_review_title"],
                content=row_as_dict["user_review_content"],
                type=ReviewType(row_as_dict["user_review_type"]),
                created_at=row_as_dict["user_review_created_at"],
            )

            rating_exists = row_as_dict["user_rating_id"] is not None
            if rating_exists:
                rating = RatingViewModel(
                    id=RatingId(row_as_dict["user_rating_id"]),
                    value=row_as_dict["user_rating_value"],
                    created_at=row_as_dict["user_rating_created_at"],
                )
            else:
                rating = None

            view_model = DetailedReviewViewModel(
                user_id=UserId(row_as_dict["user_id"]),
                review=review,
                rating=rating,
            )
            view_models.append(view_model)

        return view_models
