from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.services.base import Service
from amdb.domain.entities.series.season.season import SeriesSeason
from amdb.domain.constants import Genre, ProductionStatus
from amdb.domain.value_objects import Money, Date, Runtime


class CreateSeriesSeason(Service):

    def __call__(
        self,
        series_id: UUID,
        created_at: datetime,
        episode_count: Optional[int] = None,
        total_runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        production_status: Optional[ProductionStatus] = None,
        budget: Optional[Money] = None,
    ) -> SeriesSeason:
        return SeriesSeason(
            series_id=series_id,
            amdb_vote_count=0,
            is_under_inspection=False,
            created_at=created_at,
            episode_count=episode_count,
            amdb_rating=None,
            total_runtime=total_runtime,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            genres=genres,
            countries=countries,
            production_status=production_status,
            budget=budget,
        )
