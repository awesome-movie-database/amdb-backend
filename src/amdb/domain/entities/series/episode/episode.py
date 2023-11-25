from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset, Genre, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime
from amdb.domain.exceptions import series_episode as series_episode_exceptions


@dataclass(slots=True)
class SeriesEpisode(Entity):
    series_id: UUID
    season: int
    title: Title
    amdb_vote_count: int
    is_under_inspection: bool
    created_at: datetime

    amdb_rating: Optional[float]
    runtime: Optional[Runtime]
    release_date: Optional[Date]
    genres: Optional[list[Genre]]
    countries: Optional[list[str]]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    summary: Optional[str]
    budget: Optional[Money]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_vote_count: Optional[int]

    @classmethod
    def create(
        cls,
        series_id: UUID,
        season: int,
        title: Title,
        created_at: datetime,
        runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
    ) -> "SeriesEpisode":
        return SeriesEpisode(
            series_id=series_id,
            season=season,
            title=title,
            amdb_vote_count=0,
            is_under_inspection=False,
            created_at=created_at,
            amdb_rating=None,
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

    def update(
        self,
        title: Union[Title, Type[Unset]] = Unset,
        runtime: Union[float, None, Type[Unset]] = Unset,
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
        self._update(
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

    def add_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_episode_exceptions.SeriesEpisodeUnderInspection()

        if self.amdb_rating is None:
            self.amdb_rating = sum(votes) / len(votes)
            self.amdb_vote_count = len(votes)
            return

        self.amdb_rating = ((self.amdb_rating * self.amdb_vote_count) + sum(votes)) / (
            self.amdb_vote_count + len(votes)
        )
        self.amdb_vote_count += len(votes)

    def remove_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_episode_exceptions.SeriesEpisodeUnderInspection()

        if self.amdb_vote_count == 1:
            self.amdb_rating = None
            self.amdb_vote_count = 0
            return

        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) - sum(votes))  # type: ignore
            / (self.amdb_vote_count - len(votes))
        )
        self.amdb_vote_count -= len(votes)

    def add_to_inspection(self) -> None:
        self.is_under_inspection = True

    def remove_from_inspection(self) -> None:
        self.is_under_inspection = False
