from typing import Type, Union

from amdb.domain.services.base import Service
from amdb.domain.entities.series.episode.episode import SeriesEpisode
from amdb.domain.constants import Unset, Genre, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime


class UpdateSeriesEpisode(Service):

    def __call__(
        self,
        series_episode: SeriesEpisode,
        title: Union[Title, Type[Unset]] = Unset,
        runtime: Union[Runtime, None, Type[Unset]] = Unset,
        release_date: Union[Date, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        description: Union[str, None, Type[Unset]] = Unset,
        summary: Union[str, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        imdb_rating: Union[float, None, Type[Unset]] = Unset,
        imdb_vote_count: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        series_episode.update(
            title=title,
            runtime=runtime,
            release_date=release_date,
            genres=genres,
            countries=countries,
            production_status=production_status,
            description=description,
            summary=summary,
            budget=budget,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_vote_count=imdb_vote_count,
        )