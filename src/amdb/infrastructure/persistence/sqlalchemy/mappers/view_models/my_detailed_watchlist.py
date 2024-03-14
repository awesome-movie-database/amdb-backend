from sqlalchemy import Connection, text

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.movie_for_later import MovieForLaterId
from amdb.application.common.view_models.my_detailed_watchlist import (
    MovieViewModel,
    MovieForLaterViewModel,
    DetailedMovieForLaterViewModel,
    MyDetailedWatchlistViewModel,
)


class MyDetailedWatchlistViewModelMapper:
    def __init__(self, connecion: Connection) -> None:
        self._connection = connecion

    def get(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> MyDetailedWatchlistViewModel:
        detailed_movies_for_later = self._detailed_movies_for_later(
            current_user_id=current_user_id,
            limit=limit,
            offset=offset,
        )
        movies_for_later_count = self._movies_for_later_count(
            current_user_id=current_user_id,
        )
        view_model = MyDetailedWatchlistViewModel(
            detailed_movies_for_later=detailed_movies_for_later,
            movie_for_later_count=movies_for_later_count,
        )
        return view_model

    def _detailed_movies_for_later(
        self,
        current_user_id: UserId,
        limit: int,
        offset: int,
    ) -> list[DetailedMovieForLaterViewModel]:
        statement = text(
            """
            SELECT
                m.id movie_id,
                m.title movie_title,
                m.release_date movie_release_date,
                m.rating movie_rating,
                m.rating_count movie_rating_count,
                umfl.id movie_for_later_id,
                umfl.note movie_for_later_note,
                umfl.created_at movie_for_later_created_at
            FROM
                movies_for_later umfl
            LEFT JOIN movies m
                ON m.id = umfl.movie_id
            WHERE
                umfl.user_id = :current_user_id
            LIMIT :limit OFFSET :offset
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
            "limit": limit,
            "offset": offset,
        }
        rows = self._connection.execute(statement, parameters).fetchall()

        detailed_movies_for_later = []
        for row in rows:
            row_as_dict = row._mapping  # noqa: SLF001
            detailed_movie_for_later = DetailedMovieForLaterViewModel(
                movie=MovieViewModel(
                    id=MovieId(row_as_dict["movie_id"]),
                    title=row_as_dict["movie_title"],
                    release_date=row_as_dict["movie_release_date"],
                    rating=row_as_dict["movie_rating"],
                    rating_count=row_as_dict["movie_rating_count"],
                ),
                movie_for_later=MovieForLaterViewModel(
                    id=MovieForLaterId(row_as_dict["movie_for_later_id"]),
                    note=row_as_dict["movie_for_later_note"],
                    created_at=row_as_dict["movie_for_later_created_at"],
                ),
            )
            detailed_movies_for_later.append(detailed_movie_for_later)

        return detailed_movies_for_later

    def _movies_for_later_count(
        self,
        current_user_id: UserId,
    ) -> int:
        statement = text(
            """
            SELECT COUNT(umfl.id) FROM movies_for_later umfl
            WHERE umfl.user_id = :current_user_id
            """,
        )
        parameters = {
            "current_user_id": current_user_id,
        }
        movies_for_later_count = self._connection.execute(
            statement,
            parameters,
        ).scalar_one()

        return movies_for_later_count
