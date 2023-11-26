from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode.episode import SeriesEpisode
from amdb.domain.constants import Genre, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime


class CreateSeriesEpisode(Service):

    def __call__(
        self,
        series_id: UUID,
        season: int,
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
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
    ) -> SeriesEpisode:
        return SeriesEpisode(
            series_id=series_id,
            season=season,
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
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_vote_count=imdb_vote_count,
        )
