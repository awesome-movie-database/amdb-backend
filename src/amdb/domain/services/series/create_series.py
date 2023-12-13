from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import SeriesId, SeriesGenre, Series
from amdb.domain.constants.common import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Money


class CreateSeries(Service):
    def __call__(
        self,
        *,
        id: SeriesId,
        title: str,
        timestamp: datetime,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_rating_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_rating_count: Optional[int] = None,
    ) -> Series:
        series_genres = []
        if genres is not None:
            for genre in genres:
                series_genre = SeriesGenre(
                    genre=genre,
                    episode_count=0,
                )
                series_genres.append(series_genre)

        return Series(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
            genres=series_genres,
            countries=countries or [],
            created_at=timestamp,
            runtime=None,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            description=description,
            summary=summary,
            budget=budget,
            mpaa=mpaa,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_rating_count=kinopoisk_rating_count,
            updated_at=None,
        )
