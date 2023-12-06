from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import PersonId, Person
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
        created_at: datetime,
        genres: list[Genre] = [],
        directors: list[Person] = [],
        art_directors: list[Person] = [],
        casting_directors: list[Person] = [],
        composers: list[Person] = [],
        operators: list[Person] = [],
        producers: list[Person] = [],
        editors: list[Person] = [],
        screenwriters: list[Person] = [],
        runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        budget: Optional[Money] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_rating_count: Optional[int] = None,
    ) -> SeriesEpisode:
        series.updated_at = created_at
        season.updated_at = created_at

        self._update_series_and_series_season_genres(
            series=series,
            series_season=season,
            genres=genres,
        )

        if runtime is not None:
            self._add_runtime_to_series_and_series_season(
                series=series,
                series_season=season,
                runtime=runtime,
            )

        director_ids = self._update_persons_and_get_ids(
            persons=directors,
            updated_at=created_at,
        )
        art_director_ids = self._update_persons_and_get_ids(
            persons=art_directors,
            updated_at=created_at,
        )
        casting_director_ids = self._update_persons_and_get_ids(
            persons=casting_directors,
            updated_at=created_at,
        )
        composer_ids = self._update_persons_and_get_ids(
            persons=composers,
            updated_at=created_at,
        )
        operator_ids = self._update_persons_and_get_ids(
            persons=operators,
            updated_at=created_at,
        )
        producer_ids = self._update_persons_and_get_ids(
            persons=producers,
            updated_at=created_at,
        )
        editor_ids = self._update_persons_and_get_ids(
            persons=editors,
            updated_at=created_at,
        )
        screenwiter_ids = self._update_persons_and_get_ids(
            persons=screenwriters,
            updated_at=created_at,
        )

        return SeriesEpisode(
            series_id=series.id,
            season_number=season.number,
            number=number,
            rating=0,
            rating_count=0,
            genres=genres,
            director_ids=director_ids,
            art_director_ids=art_director_ids,
            casting_director_ids=casting_director_ids,
            composer_ids=composer_ids,
            operator_ids=operator_ids,
            producer_ids=producer_ids,
            editor_ids=editor_ids,
            screenwriter_ids=screenwiter_ids,
            created_at=created_at,
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
            for series_genre in series.genres:
                if series_genre.genre == genre:
                    series_genre.episode_count += 1
                else:
                    series.genres.append(
                        SeriesGenre(
                            genre=genre,
                            episode_count=1,
                        )
                    )
            for series_season_genre in series_season.genres:
                if series_season_genre.genre == genre:
                    series_season_genre.episode_count += 1
                else:
                    series_season.genres.append(
                        SeriesSeasonGenre(
                            genre=genre,
                            episode_count=1,
                        )
                    )

    def _add_runtime_to_series_and_series_season(
        self,
        *,
        series: Series,
        series_season: SeriesSeason,
        runtime: Runtime,
    ) -> None:
        if series_season.runtime is None:
            series_season.runtime = runtime
        else:
            series_season.runtime += runtime

        if series.runtime is None:
            series.runtime = runtime
        else:
            series.runtime += runtime

    def _update_persons_and_get_ids(
        self,
        *,
        persons: list[Person],
        updated_at: datetime,
    ) -> list[PersonId]:
        person_ids = []
        for person in persons:
            person_ids.append(person.id)
            person.updated_at = updated_at

        return person_ids
