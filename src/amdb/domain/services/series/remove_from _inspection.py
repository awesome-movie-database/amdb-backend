from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.exceptions.series import SeriesNotUnderInspection


class RemoveSeriesFromInspection(Service):

    def __call__(
        self,
        series: Series,
    ) -> None:
        if not series.is_under_inspection:
            raise SeriesNotUnderInspection()
        series.is_under_inspection = False