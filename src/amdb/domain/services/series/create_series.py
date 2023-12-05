from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.series.series import SeriesId, SeriesTitle, Series
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


class CreateSeries(Service):
    def __call__(
        self,
        *,
        id: SeriesId,
        title: SeriesTitle,
        created_at: datetime,
        genres: list[Genre] = [],
        countries: list[str] = [],
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
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_vote_count: Optional[int] = None,
    ) -> Series:
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

        return Series(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
            genres=genres,
            countries=countries,
            created_at=created_at,
            runtime=runtime,
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
            imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
            updated_at=None,
        )
