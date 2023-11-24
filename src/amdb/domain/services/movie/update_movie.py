from typing import Type, Union

from amdb.domain.entities.movie.movie import Movie
from amdb.domain.services.base import Service
from amdb.domain.constants import Genre, MPAA, ProductionStatus, Unset
from amdb.domain.value_objects import Date, Money, Runtime, Title


class UpdateMovie(Service):

    def __call__(
        self,
        movie: Movie,
        title: Union[Title, Type[Unset]] = Unset,
        runtime: Union[Runtime, None, Type[Unset]] = Unset,
        release_date: Union[Date, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        description: Union[str, None, Type[Unset]] = Unset,
        summary: Union[str, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
        revenue: Union[Money, None, Type[Unset]] = Unset,
        mpaa: Union[MPAA, None, Type[Unset]] = Unset,
        filming_start: Union[Date, None, Type[Unset]] = Unset,
        filming_end: Union[Date, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        imdb_rating: Union[float, None, Type[Unset]] = Unset,
        imdb_vote_count: Union[int, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_rating: Union[float, None, Type[Unset]] = Unset,
        kinopoisk_vote_count: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        movie.update(
            title=title,
            runtime=runtime,
            release_date=release_date,
            genres=genres,
            countries=countries,
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
            imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
        )
