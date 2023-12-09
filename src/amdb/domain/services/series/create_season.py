from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.constants import ProductionStatus
from amdb.domain.value_objects import Date, Money


class CreateSeriesSeason(Service):
    def __call__(
        self,
        *,
        series: Series,
        number: int,
        timestamp: datetime,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        production_status: Optional[ProductionStatus] = None,
        budget: Optional[Money] = None,
    ) -> SeriesSeason:
        series.updated_at = timestamp

        return SeriesSeason(
            series_id=series.id,
            number=number,
            rating=0,
            rating_count=0,
            genres=[],
            created_at=timestamp,
            runtime=None,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            budget=budget,
            updated_at=None,
        )
