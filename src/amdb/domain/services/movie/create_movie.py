from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.services.base import Service
from amdb.domain.entities.movie.movie import Movie
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Money, Runtime, Title


class CreateMovie(Service):

    def __call__(
        self,
        id: UUID,
        title: Title,
        created_at: datetime,
        runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
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
        imdb_vote_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_vote_count: Optional[int]  = None,
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            amdb_vote_count=0,
            is_under_inspection=False,
            created_at=created_at,
            amdb_rating=None,
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