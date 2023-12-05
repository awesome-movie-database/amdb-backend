from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.constants import Unset, unset, ProductionStatus
from amdb.domain.value_objects import Date


class UpdateSeriesSeason(Service):
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        updated_at: datetime,
        number: Union[ProductionStatus, Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        end_date: Union[Date, None, Unset] = unset,
        is_ongoing: Union[bool, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
    ) -> None:
        series.updated_at = updated_at

        self._update_entity(
            entity=season,
            number=number,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            updated_at=updated_at,
        )
