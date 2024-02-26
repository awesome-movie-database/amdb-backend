from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId
from amdb.application.common.view_models.my_detailed_ratings import (
    MovieViewModel,
    RatingViewModel,
    DetailedRatingViewModel,
    MyDetailedRatingsViewModel,
)


class MyDetailedRatingsViewModelMapper:
    def __init__(self, connecion: Connection) -> None:
        self._connection = connecion

    def get(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> MyDetailedRatingsViewModel:
        detailed_ratings = self._detailed_ratings(
            current_user_id=current_user_id,
            limit=limit,
            offset=offset,
        )
        rating_count = self._rating_count(
            current_user_id=current_user_id,
        )
        view_model = MyDetailedRatingsViewModel(
            detailed_ratings=detailed_ratings,
            rating_count=rating_count,
        )
        return view_model

    def _detailed_ratings(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> list[DetailedRatingViewModel]:
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
                urt.created_at user_rating_created_at
            FROM
                ratings urt
            LEFT JOIN movies m
                ON m.id = urt.movie_id
            WHERE
                urt.user_id = :current_user_id
            LIMIT :limit OFFSET :offset
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
            "limit": limit,
            "offset": offset,
        }
        rows = self._connection.execute(statement, parameters).fetchall()

        detailed_ratings = []
        for row in rows:
            row_as_dict = row._mapping  # noqa: SLF001
            detailed_rating = DetailedRatingViewModel(
                movie=MovieViewModel(
                    id=MovieId(row_as_dict["movie_id"]),
                    title=row_as_dict["movie_title"],
                    release_date=row_as_dict["movie_release_date"],
                    rating=row_as_dict["movie_rating"],
                    rating_count=row_as_dict["movie_rating_count"],
                ),
                rating=RatingViewModel(
                    id=RatingId(row_as_dict["user_rating_id"]),
                    value=row_as_dict["user_rating_value"],
                    created_at=row_as_dict["user_rating_created_at"],
                ),
            )
            detailed_ratings.append(detailed_rating)

        return detailed_ratings

    def _rating_count(self, current_user_id: UserId) -> int:
        statement = text(
            """
            SELECT COUNT(urt.id) FROM ratings urt
            WHERE urt.user_id = :current_user_id
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
        }
        rating_count = self._connection.execute(
            statement,
            parameters,
        ).scalar_one()
        return rating_count
