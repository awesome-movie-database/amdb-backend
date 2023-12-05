from dataclasses import dataclass
from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.movie.movie import Movie, MovieTitle
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
        updated_at: datetime,
        title: Union[MovieTitle, Unset] = unset,
        genres: Union[list[Genre], Unset] = unset,
        countries: Union[list[str], Unset] = unset,
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
        if directors is not unset:
            director_ids = [director.id for director in directors.new_directors]
            self._update_persons(
                old_persons=directors.old_directors,
                new_persons=directors.new_directors,
                updated_at=updated_at,
            )
        else:
            director_ids = movie.director_ids

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
            art_director_ids = movie.art_director_ids

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
            casting_director_ids = movie.casting_director_ids

        if composers is not unset:
            composer_ids = [composer.id for composer in composers.new_composers]
            self._update_persons(
                old_persons=composers.old_composers,
                new_persons=composers.new_composers,
                updated_at=updated_at,
            )
        else:
            composer_ids = movie.composer_ids

        if operators is not unset:
            operator_ids = [operator.id for operator in operators.new_operators]
            self._update_persons(
                old_persons=operators.old_operators,
                new_persons=operators.new_operators,
                updated_at=updated_at,
            )
        else:
            operator_ids = movie.operator_ids

        if producers is not unset:
            producer_ids = [producer.id for producer in producers.new_producers]
            self._update_persons(
                old_persons=producers.old_producers,
                new_persons=producers.new_producers,
                updated_at=updated_at,
            )
        else:
            producer_ids = movie.producer_ids

        if editors is not unset:
            editor_ids = [editor.id for editor in editors.new_editors]
            self._update_persons(
                old_persons=editors.old_editors,
                new_persons=editors.new_editors,
                updated_at=updated_at,
            )
        else:
            editor_ids = movie.editor_ids

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
            screenwriter_ids = movie.screenwriter_ids

        self._update_entity(
            entity=movie,
            title=title,
            genres=genres,
            countries=countries,
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
            updated_at=updated_at,
        )

    def _update_persons(
        self,
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
