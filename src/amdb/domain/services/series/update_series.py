from typing import Type, Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.constants import Genre, MPAA, ProductionStatus, Unset
from amdb.domain.value_objects import Date, Money, Runtime, Title


class UpdateSeries(Service):

    def __call__(
        self,
        series: Series,
        title: Union[Title, Type[Unset]] = Unset,
        season_count: Union[int, None, Type[Unset]] = Unset,
        episode_count: Union[int, None, Type[Unset]] = Unset,
        total_runtime: Union[Runtime, None, Type[Unset]] = Unset,
        release_date: Union[Date, None, Type[Unset]] = Unset,
        end_date: Union[Date, None, Type[Unset]] = Unset,
        is_ongoing: Union[bool, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        description: Union[str, None, Type[Unset]] = Unset,
        summary: Union[str, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
        mpaa: Union[MPAA, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        imdb_rating: Union[float, None, Type[Unset]] = Unset,
        imdb_vote_count: Union[int, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_rating: Union[float, None, Type[Unset]] = Unset,
        kinopoisk_vote_count: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        series.update(
            title=title,
            season_count=season_count,
            episode_count=episode_count,
            total_runtime=total_runtime,
            release_date=release_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            genres=genres,
            countries=countries,
            production_status=production_status,
            description=description,
            summary=summary,
            budget=budget,
            mpaa=mpaa,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
        )
