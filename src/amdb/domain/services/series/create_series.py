from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Money, Runtime, Title


class CreateSeries(Service):

    def __call__(
        self,
        id: UUID,
        title: Title,
        created_at: datetime,
        season_count: Optional[int] = None,
        episode_count: Optional[int] = None,
        amdb_rating: Optional[float] = None,
        total_runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
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
        return Series(
            id=id,
            title=title,
            amdb_vote_count=0,
            is_under_inspection=False,
            created_at=created_at,
            season_count=season_count,
            episode_count=episode_count,
            amdb_rating=None,
            total_runtime=total_runtime,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            genres=genres,
            countries=countries,
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
        )
