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
        title: Union[SeriesTitle, Unset] = unset,
        countries: Union[list[str], Unset] = unset,
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
        self._update_entity(
            entity=series,
            title=title,
            countries=countries,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            production_status=production_status,
            description=description,
            summary=summary,
            mpaa=mpaa,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_rating_count=imdb_rating_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_rating_count=kinopoisk_rating_count,
            updated_at=updated_at,
        )
