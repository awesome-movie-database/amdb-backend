from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import SeriesGenre, Series
from amdb.domain.constants import Unset, unset, Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date
from amdb.domain.exceptions.series import UpdateSeriesError


class UpdateSeries(Service):
    def __call__(
        self,
        *,
        series: Series,
        timestamp: datetime,
        title: Union[str, Unset] = unset,
        genres: Union[list[Genre], Unset] = unset,
        countries: Union[list[str], Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        end_date: Union[Date, None, Unset] = unset,
        is_ongoing: Union[bool, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        summary: Union[str, None, Unset] = unset,
        mpaa: Union[MPAA, None, Unset] = unset,
        imdb_id: Union[str, None, Unset] = unset,
        imdb_rating: Union[float, None, Unset] = unset,
        imdb_rating_count: Union[int, None, Unset] = unset,
        kinopoisk_id: Union[str, None, Unset] = unset,
        kinopoisk_rating: Union[float, None, Unset] = unset,
        kinopoisk_rating_count: Union[int, None, Unset] = unset,
    ) -> None:
        if genres is not unset:
            series_genres = self._get_updated_series_genres(
                series=series,
                genres=genres,
            )
        else:
            series_genres = series.genres

        self._update_entity(
            entity=series,
            title=title,
            genres=series_genres,
            countries=countries,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            description=description,
            summary=summary,
            mpaa=mpaa,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_rating_count=kinopoisk_rating_count,
            updated_at=timestamp,
        )

    def _get_updated_series_genres(
        self,
        *,
        series: Series,
        genres: list[Genre],
    ) -> list[SeriesGenre]:
        updated_series_genres = series.genres.copy()

        # Remove genres
        for series_genre in series.genres:
            if series_genre.genre not in genres:
                if series_genre.episode_count != 0:
                    raise UpdateSeriesError()
                updated_series_genres.remove(series_genre)

        # Add genres
        series_genres_genres = [series_genre.genre for series_genre in series.genres]
        for genre in genres:
            if genre not in series_genres_genres:
                updated_series_genres.append(
                    SeriesGenre(
                        genre=genre,
                        episode_count=0,
                    ),
                )

        return updated_series_genres
