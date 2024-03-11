from typing import Optional

from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.domain.entities.review import ReviewId, ReviewType
from amdb.application.common.view_models.detailed_movie import (
    MovieViewModel,
    UserRatingViewModel,
    UserReviewViewModel,
    DetailedMovieViewModel,
)


class DetailedMovieViewModelMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def get(
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
                AND urt.movie_id = m.id
            LEFT JOIN reviews urv
                ON urv.user_id = :current_user_id
                AND urv.movie_id = m.id
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
            row_as_dict = row._mapping  # noqa: SLF001

            movie = MovieViewModel(
                id=MovieId(row_as_dict["movie_id"]),
                title=row_as_dict["movie_title"],
                release_date=row_as_dict["movie_release_date"],
                rating=row_as_dict["movie_rating"],
                rating_count=row_as_dict["movie_rating_count"],
            )

            rating_exists = row_as_dict["user_rating_id"] is not None
            if rating_exists:
                user_rating = UserRatingViewModel(
                    id=RatingId(row_as_dict["user_rating_id"]),
                    value=row_as_dict["user_rating_value"],
                    created_at=row_as_dict["user_rating_created_at"],
                )
            else:
                user_rating = None

            review_exists = row_as_dict["user_review_id"] is not None
            if review_exists:
                user_review = UserReviewViewModel(
                    id=ReviewId(row_as_dict["user_review_id"]),
                    title=row_as_dict["user_review_title"],
                    content=row_as_dict["user_review_content"],
                    type=ReviewType(row_as_dict["user_review_type"]),
                    created_at=row_as_dict["user_review_created_at"],
                )
            else:
                user_review = None

            view_model = DetailedMovieViewModel(
                movie=movie,
                user_rating=user_rating,
                user_review=user_review,
            )
            return view_model
        return None
