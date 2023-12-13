from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.constants.common import Unset, unset, Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


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
