from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.application.common.view_models.rating_for_export import (
    MovieViewModel,
    RatingViewModel,
    RatingForExportViewModel,
)


class RatingForExportViewModelMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def get(
        self,
        current_user_id: UserId,
    ) -> list[RatingForExportViewModel]:
        statement = text(
            """
            SELECT
                m.id movie_id,
                m.title movie_title,
                m.release_date movie_release_date,
                m.rating movie_rating,
                m.rating_count movie_rating_count,
                urt.value user_rating_value,
                urt.created_at user_rating_created_at
            FROM
                ratings urt
            LEFT JOIN movies m
                ON m.id = urt.movie_id
            WHERE
                urt.user_id = :current_user_id
            """,
        )
        parameters = {"current_user_id": current_user_id}
        rows = self._connection.execute(statement, parameters).fetchall()

        view_models = []
        for row in rows:
            row_as_dict = row._mapping  # noqa: SLF001

            movie = MovieViewModel(
                id=row_as_dict["movie_id"],
                title=row_as_dict["movie_title"],
                release_date=row_as_dict["movie_release_date"],
                rating=row_as_dict["movie_rating"],
                rating_count=row_as_dict["movie_rating_count"],
            )
            rating = RatingViewModel(
                value=row_as_dict["user_rating_value"],
                created_at=row_as_dict["user_rating_created_at"],
            )
            view_model = RatingForExportViewModel(
                movie=movie,
                rating=rating,
            )
            view_models.append(view_model)

        return view_models
