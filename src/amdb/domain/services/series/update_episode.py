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
        updated_at: datetime,
        number: Union[int, Unset] = unset,
        genres: Union[list[Genre], Unset] = unset,
        directors: Union[Directors, Unset] = unset,
        art_directors: Union[ArtDirectors, Unset] = unset,
        casting_directors: Union[CastingDirectors, Unset] = unset,
        composers: Union[Composers, Unset] = unset,
        operators: Union[Operators, Unset] = unset,
        producers: Union[Producers, Unset] = unset,
        editors: Union[Editors, Unset] = unset,
        screenwriters: Union[Screenwriters, Unset] = unset,
        runtime: Union[Runtime, None, Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        budget: Union[Money, None, Unset] = unset,
        imdb_id: Union[str, None, Unset] = unset,
        imdb_rating: Union[float, None, Unset] = unset,
        imdb_rating_count: Union[int, None, Unset] = unset,
    ) -> None:
        series.updated_at = updated_at
        season.updated_at = updated_at

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

        if directors is not unset:
            director_ids = [director.id for director in directors.new_directors]
            self._update_persons(
                old_persons=directors.old_directors,
                new_persons=directors.new_directors,
                updated_at=updated_at,
            )
        else:
            director_ids = episode.director_ids

        if art_directors is not unset:
            art_director_ids = [
                art_director.id for art_director in art_directors.new_art_directors
            ]
            self._update_persons(
                old_persons=art_directors.old_art_directors,
                new_persons=art_directors.new_art_directors,
                updated_at=updated_at,
            )
        else:
            art_director_ids = episode.art_director_ids

        if casting_directors is not unset:
            casting_director_ids = [
                casting_director.id for casting_director in casting_directors.new_casting_directors
            ]
            self._update_persons(
                old_persons=casting_directors.old_casting_directors,
                new_persons=casting_directors.new_casting_directors,
                updated_at=updated_at,
            )
        else:
            casting_director_ids = episode.casting_director_ids

        if composers is not unset:
            composer_ids = [composer.id for composer in composers.new_composers]
            self._update_persons(
                old_persons=composers.old_composers,
                new_persons=composers.new_composers,
                updated_at=updated_at,
            )
        else:
            composer_ids = episode.composer_ids

        if operators is not unset:
            operator_ids = [operator.id for operator in operators.new_operators]
            self._update_persons(
                old_persons=operators.old_operators,
                new_persons=operators.new_operators,
                updated_at=updated_at,
            )
        else:
            operator_ids = episode.operator_ids

        if producers is not unset:
            producer_ids = [producer.id for producer in producers.new_producers]
            self._update_persons(
                old_persons=producers.old_producers,
                new_persons=producers.new_producers,
                updated_at=updated_at,
            )
        else:
            producer_ids = episode.producer_ids

        if editors is not unset:
            editor_ids = [editor.id for editor in editors.new_editors]
            self._update_persons(
                old_persons=editors.old_editors,
                new_persons=editors.new_editors,
                updated_at=updated_at,
            )
        else:
            editor_ids = episode.editor_ids

        if screenwriters is not unset:
            screenwriter_ids = [
                screenwriter.id for screenwriter in screenwriters.new_screenwriters
            ]
            self._update_persons(
                old_persons=screenwriters.old_screenwriters,
                new_persons=screenwriters.new_screenwriters,
                updated_at=updated_at,
            )
        else:
            screenwriter_ids = episode.screenwriter_ids

        self._update_entity(
            entity=episode,
            number=number,
            genres=genres,
            director_ids=director_ids,
            art_director_ids=art_director_ids,
            casting_director_ids=casting_director_ids,
            composer_ids=composer_ids,
            operator_ids=operator_ids,
            producer_ids=producer_ids,
            editor_ids=editor_ids,
            screenwriter_ids=screenwriter_ids,
            runtime=runtime,
            release_date=release_date,
            production_status=production_status,
            description=description,
            budget=budget,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
        )

    def _update_persons(
        self,
        *,
        old_persons: list[Person],
        new_persons: list[Person],
        updated_at: datetime,
    ) -> None:
        for old_person in old_persons:
            if old_person in new_persons:
                continue
            old_person.updated_at = updated_at

        for new_person in new_persons:
            if new_person in old_persons:
                continue
            new_person.updated_at = updated_at

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
