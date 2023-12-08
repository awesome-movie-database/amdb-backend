from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.movie.movie import MovieId, MovieTitle, Movie
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


class CreateMovie(Service):
    def __call__(
        self,
        *,
        id: MovieId,
        title: MovieTitle,
        created_at: datetime,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        directors: Optional[list[Person]] = None,
        art_directors: Optional[list[Person]] = None,
        casting_directors: Optional[list[Person]] = None,
        composers: Optional[list[Person]] = None,
        operators: Optional[list[Person]] = None,
        producers: Optional[list[Person]] = None,
        editors: Optional[list[Person]] = None,
        screenwriters: Optional[list[Person]] = None,
        runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        revenue: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        filming_start: Optional[Date] = None,
        filming_end: Optional[Date] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_rating_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_rating_count: Optional[int] = None,
    ) -> Movie:
        director_ids = self._update_persons_and_get_ids(
            persons=directors or [],
            updated_at=created_at,
        )
        art_director_ids = self._update_persons_and_get_ids(
            persons=art_directors or [],
            updated_at=created_at,
        )
        casting_director_ids = self._update_persons_and_get_ids(
            persons=casting_directors or [],
            updated_at=created_at,
        )
        composer_ids = self._update_persons_and_get_ids(
            persons=composers or [],
            updated_at=created_at,
        )
        operator_ids = self._update_persons_and_get_ids(
            persons=operators or [],
            updated_at=created_at,
        )
        producer_ids = self._update_persons_and_get_ids(
            persons=producers or [],
            updated_at=created_at,
        )
        editor_ids = self._update_persons_and_get_ids(
            persons=editors or [],
            updated_at=created_at,
        )
        screenwiter_ids = self._update_persons_and_get_ids(
            persons=screenwriters or [],
            updated_at=created_at,
        )

        return Movie(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
            genres=genres or [],
            countries=countries or [],
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
            summary=summary,
            budget=budget,
            revenue=revenue,
            mpaa=mpaa,
            filming_start=filming_start,
            filming_end=filming_end,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_rating_count=kinopoisk_rating_count,
            updated_at=None,
        )

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
