from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import MovieId, Movie
from amdb.domain.constants.common import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


class CreateMovie(Service):
    def __call__(
        self,
        *,
        id: MovieId,
        title: str,
        timestamp: datetime,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
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
        return Movie(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
            genres=genres or [],
            countries=countries or [],
            created_at=timestamp,
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
