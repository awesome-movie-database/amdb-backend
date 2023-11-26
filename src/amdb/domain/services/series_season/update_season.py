from typing import Type, Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.season.season import SeriesSeason
from amdb.domain.constants import Genre, ProductionStatus, Unset
from amdb.domain.value_objects import Money, Date, Runtime


class UpdateSeriesSeason(Service):

    def __call__(
        self,
        series_season: SeriesSeason,
        episode_count: Union[int, None, Type[Unset]] = Unset,
        total_runtime: Union[Runtime, None, Type[Unset]] = Unset,
        release_date: Union[Date, None, Type[Unset]] = Unset,
        end_date: Union[Date, None, Type[Unset]] = Unset,
        is_ongoing: Union[bool, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
    ) -> None:
        series_season.update(
            episode_count=episode_count,
            total_runtime=total_runtime,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            genres=genres,
            countries=countries,
            production_status=production_status,
            budget=budget,
        )