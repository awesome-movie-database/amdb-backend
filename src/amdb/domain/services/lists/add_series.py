from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.lists.list import List
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.lists.series import ListSeries


class AddSeriesToList(Service):
    def __call__(
        self,
        *,
        list: List,
        series: Series,
        created_at: datetime,
    ) -> ListSeries:
        list.updated_at = created_at

        return ListSeries(
            list_id=list.id,
            series_id=series.id,
            created_at=created_at,
        )
