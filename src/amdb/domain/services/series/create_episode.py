from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
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
        imdb_vote_count: Optional[int] = None,
    ) -> SeriesEpisode:
        series.updated_at = created_at
        season.updated_at = created_at

        for genre in genres:
            if genre not in season.genres:
                season.genres.append(genre)
            if genre not in series.genres:
                series.genres.append(genre)

        if runtime is not None:
            if season.runtime is None:
                season.runtime = runtime
            else:
                season.runtime += runtime

            if series.runtime is None:
                series.runtime = runtime
            else:
                series.runtime += runtime

        if budget is not None:
            if season.budget is None:
                season.budget = budget
            else:
                season.budget += budget

            if series.budget is None:
                series.budget = budget
            else:
                series.budget += budget

        director_ids = []
        for director in directors:
            director_ids.append(director.id)
            director.updated_at = created_at

        art_director_ids = []
        for art_director in art_directors:
            art_director_ids.append(art_director.id)
            art_director.updated_at = created_at

        casting_director_ids = []
        for casting_director in casting_directors:
            casting_director_ids.append(casting_director.id)
            casting_director.updated_at = created_at

        composer_ids = []
        for composer in composers:
            composer_ids.append(composer.id)
            composer.updated_at = created_at

        operator_ids = []
        for operator in operators:
            operator_ids.append(operator.id)
            operator.updated_at = created_at

        producer_ids = []
        for producer in producers:
            producer_ids.append(producer.id)
            producer.updated_at = created_at

        editor_ids = []
        for editor in editors:
            editor_ids.append(editor.id)
            editor.updated_at = created_at

        screenwiter_ids = []
        for screenwiter in screenwriters:
            screenwiter_ids.append(screenwiter.id)
            screenwiter.updated_at = created_at

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
            imdb_vote_count=imdb_vote_count,
            updated_at=None,
        )
