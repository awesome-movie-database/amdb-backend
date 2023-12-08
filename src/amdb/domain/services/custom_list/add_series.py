from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.custom_list.custom_list import CustomList
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.custom_list.series import CustomListSeries


class AddSeriesToList(Service):
    def __call__(
        self,
        *,
        custom_list: CustomList,
        series: Series,
        created_at: datetime,
    ) -> CustomListSeries:
        custom_list.updated_at = created_at

        return CustomListSeries(
            custom_list_id=custom_list.id,
            series_id=series.id,
            created_at=created_at,
        )
