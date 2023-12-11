from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import SeriesGenre, Series
from amdb.domain.entities.series.season import SeriesSeasonGenre, SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.constants import Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


class CreateSeriesEpisode(Service):
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        number: int,
        timestamp: datetime,
        genres: Optional[list[Genre]] = None,
        runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        budget: Optional[Money] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_rating_count: Optional[int] = None,
    ) -> SeriesEpisode:
        series.updated_at = timestamp
        season.updated_at = timestamp

        self._update_series_and_series_season_genres(
            series=series,
            series_season=season,
            genres=genres or [],
        )

        if runtime is not None:
            self._add_runtime_to_series(
                series=series,
                runtime=runtime,
            )
            self._add_runtime_to_series_season(
                series_season=season,
                runtime=runtime,
            )

        return SeriesEpisode(
            series_id=series.id,
            season_number=season.number,
            number=number,
            rating=0,
            rating_count=0,
            genres=genres or [],
            created_at=timestamp,
            runtime=runtime,
            release_date=release_date,
            production_status=production_status,
            description=description,
            budget=budget,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
            updated_at=None,
        )

    def _update_series_and_series_season_genres(
        self,
        *,
        series: Series,
        series_season: SeriesSeason,
        genres: list[Genre],
    ) -> None:
        for genre in genres:
            self._add_genre_to_series(
                series=series,
                genre=genre,
            )
            self._add_genre_to_series_season(
                series_season=series_season,
                genre=genre,
            )

    def _add_genre_to_series(
        self,
        *,
        series: Series,
        genre: Genre,
    ) -> None:
        for series_genre in series.genres:
            if series_genre.genre == genre:
                series_genre.episode_count += 1
            else:
                series.genres.append(
                    SeriesGenre(
                        genre=genre,
                        episode_count=1,
                    ),
                )

    def _add_genre_to_series_season(
        self,
        *,
        series_season: SeriesSeason,
        genre: Genre,
    ) -> None:
        for series_season_genre in series_season.genres:
            if series_season_genre.genre == genre:
                series_season_genre.episode_count += 1
            else:
                series_season.genres.append(
                    SeriesSeasonGenre(
                        genre=genre,
                        episode_count=1,
                    ),
                )

    def _add_runtime_to_series(
        self,
        *,
        series: Series,
        runtime: Runtime,
    ) -> None:
        if series.runtime is None:
            series.runtime = runtime
        else:
            series.runtime += runtime

    def _add_runtime_to_series_season(
        self,
        *,
        series_season: SeriesSeason,
        runtime: Runtime,
    ) -> None:
        if series_season.runtime is None:
            series_season.runtime = runtime
        else:
            series_season.runtime += runtime
