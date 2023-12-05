from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import SeriesTitle, Series
from amdb.domain.constants import Unset, unset, MPAA, ProductionStatus
from amdb.domain.value_objects import Date


class UpdateSeries(Service):
    def __call__(
        self,
        *,
        series: Series,
        updated_at: datetime,
        countries: Union[list[str], Unset] = unset,
        title: Union[SeriesTitle, Unset] = unset,
        release_date: Union[Date, None, Unset] = unset,
        end_date: Union[Date, None, Unset] = unset,
        is_ongoing: Union[bool, None, Unset] = unset,
        production_status: Union[ProductionStatus, None, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        summary: Union[str, None, Unset] = unset,
        mpaa: Union[MPAA, None, Unset] = unset,
        imdb_id: Union[str, None, Unset] = unset,
        imdb_rating: Union[float, None, Unset] = unset,
        imdb_rating_count: Union[int, None, Unset] = unset,
        kinopoisk_id: Union[str, None, Unset] = unset,
        kinopoisk_rating: Union[float, None, Unset] = unset,
        kinopoisk_rating_count: Union[int, None, Unset] = unset,
    ) -> None:
        ...
