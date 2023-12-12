from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.series.series import SeriesGenre, Series
from amdb.domain.entities.series.season import SeriesSeasonGenre, SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.constants import Unset, unset, Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


@dataclass(frozen=True, slots=True)
class Directors:
    old_directors: list[Person]
    new_directors: list[Person]


@dataclass(frozen=True, slots=True)
class ArtDirectors:
    old_art_directors: list[Person]
    new_art_directors: list[Person]


@dataclass(frozen=True, slots=True)
class CastingDirectors:
    old_casting_directors: list[Person]
    new_casting_directors: list[Person]


@dataclass(frozen=True, slots=True)
class Composers:
    old_composers: list[Person]
    new_composers: list[Person]


@dataclass(frozen=True, slots=True)
class Operators:
    old_operators: list[Person]
    new_operators: list[Person]


@dataclass(frozen=True, slots=True)
class Producers:
    old_producers: list[Person]
    new_producers: list[Person]


@dataclass(frozen=True, slots=True)
class Editors:
    old_editors: list[Person]
    new_editors: list[Person]


@dataclass(frozen=True, slots=True)
class Screenwriters:
    old_screenwriters: list[Person]
    new_screenwriters: list[Person]


class UpdateSeriesEpisode(Service):
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        episode: SeriesEpisode,
        timestamp: datetime,
        number: Union[int, Unset] = unset,
        genres: Union[list[Genre], Unset] = unset,
        runtime: Union[Runtime, None, Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        budget: Union[Money, None, Unset] = unset,
        imdb_id: Union[str, None, Unset] = unset,
        imdb_rating: Union[float, None, Unset] = unset,
        imdb_rating_count: Union[int, None, Unset] = unset,
    ) -> None:
        series.updated_at = timestamp
        season.updated_at = timestamp

        if genres is not unset:
            self._update_series_and_series_season_genres(
                series=series,
                series_season=season,
                series_episode=episode,
                genres=genres,
            )
        if runtime is not unset:
            self._update_series_runtime(
                series=series,
                episode=episode,
                runtime=runtime,
            )
            self._update_series_season_runtime(
                series_season=season,
                episode=episode,
                runtime=runtime,
            )

        self._update_entity(
            entity=episode,
            number=number,
            genres=genres,
            runtime=runtime,
            release_date=release_date,
            production_status=production_status,
            description=description,
            budget=budget,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
        )

    def _update_series_and_series_season_genres(
        self,
        *,
        series: Series,
        series_season: SeriesSeason,
        series_episode: SeriesEpisode,
        genres: list[Genre],
    ) -> None:
        for series_episode_genre in series_episode.genres:
            if series_episode_genre not in genres:
                self._remove_genre_from_series(
                    series=series,
                    genre=series_episode_genre,
                )
                self._remove_genre_from_series_season(
                    series_season=series_season,
                    genre=series_episode_genre,
                )
        for genre in genres:
            if genre not in series_episode.genres:
                self._add_genre_to_series(
                    series=series,
                    genre=genre,
                )
                self._add_genre_to_series_season(
                    series_season=series_season,
                    genre=genre,
                )

    def _remove_genre_from_series(
        self,
        *,
        series: Series,
        genre: Genre,
    ) -> None:
        for series_genre in series.genres:
            if series_genre.genre == genre:
                series_genre.episode_count -= 1
                updated_series_genre = series_genre
                break
        if updated_series_genre.episode_count == 0:
            series.genres.remove(updated_series_genre)

    def _remove_genre_from_series_season(
        self,
        *,
        series_season: SeriesSeason,
        genre: Genre,
    ) -> None:
        for series_season_genre in series_season.genres:
            if series_season_genre.genre == genre:
                series_season_genre.episode_count -= 1
                updated_series_season_genre = series_season_genre
                break
        if updated_series_season_genre.episode_count == 0:
            series_season.genres.remove(updated_series_season_genre)

    def _add_genre_to_series(
        self,
        *,
        series: Series,
        genre: Genre,
    ) -> None:
        for series_genre in series.genres:
            if series_genre.genre == genre:
                series_genre.episode_count += 1
                break
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
                break
        else:
            series_season.genres.append(
                SeriesSeasonGenre(
                    genre=genre,
                    episode_count=1,
                ),
            )

    def _update_series_runtime(
        self,
        *,
        series: Series,
        episode: SeriesEpisode,
        runtime: Optional[Runtime],
    ) -> None:
        if series.runtime is None:
            series.runtime = runtime
            return

        series.runtime -= episode.runtime
        if runtime is not None:
            series.runtime += runtime

    def _update_series_season_runtime(
        self,
        *,
        series_season: SeriesSeason,
        episode: SeriesEpisode,
        runtime: Optional[Runtime],
    ) -> None:
        if series_season.runtime is None:
            series_season.runtime = runtime
            return

        series_season.runtime -= episode.runtime
        if runtime is not None:
            series_season.runtime += runtime
