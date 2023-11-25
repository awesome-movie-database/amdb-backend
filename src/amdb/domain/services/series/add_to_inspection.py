from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.exceptions.series import SeriesUnderInspection


class AddSeriesToInspection(Service):

    def __call__(
        self,
        series: Series,
    ) -> None:
        if series.is_under_inspection:
            raise SeriesUnderInspection()
        series.is_under_inspection = True
