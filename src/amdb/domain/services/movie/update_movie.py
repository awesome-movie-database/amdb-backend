from dataclasses import dataclass
from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.constants import Unset, unset, Genre, MPAA, ProductionStatus
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


class UpdateMovie(Service):
    def __call__(
        self,
        *,
        movie: Movie,
        timestamp: datetime,
        title: Union[str, Unset] = unset,
        genres: Union[list[Genre], Unset] = unset,
        countries: Union[list[str], Unset] = unset,
        runtime: Union[Runtime, None, Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        summary: Union[str, None, Unset] = unset,
        budget: Union[Money, None, Unset] = unset,
        revenue: Union[Money, None, Unset] = unset,
        mpaa: Union[MPAA, None, Unset] = unset,
        filming_start: Union[Date, None, Unset] = unset,
        filming_end: Union[Date, None, Unset] = unset,
        imdb_id: Union[str, None, Unset] = unset,
        imdb_rating: Union[float, None, Unset] = unset,
        imdb_rating_count: Union[int, None, Unset] = unset,
        kinopoisk_id: Union[str, None, Unset] = unset,
        kinopoisk_rating: Union[float, None, Unset] = unset,
        kinopoisk_rating_count: Union[int, None, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=movie,
            title=title,
            genres=genres,
            countries=countries,
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
            imdb_vote_count=imdb_rating_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_rating_count,
            updated_at=timestamp,
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
