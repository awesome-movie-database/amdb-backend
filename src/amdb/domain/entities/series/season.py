from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset, Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money
from amdb.domain.exceptions.series import season as series_season_exceptions


@dataclass(slots=True)
class SeriesSeason(Entity):

    series_id: UUID
    amdb_vote_count: int
    is_under_inspection: bool
    created_at: datetime

    episode_count: Optional[int]
    amdb_rating: Optional[float]
    total_runtime: Optional[Runtime]
    release_date: Optional[Date]
    end_date: Optional[Date]
    is_ongoing: Optional[bool]
    genres: Optional[list[Genre]]
    countries: Optional[list[str]]
    production_status: Optional[ProductionStatus]
    budget: Optional[Money]

    @classmethod
    def create(
        cls,
        series_id: UUID,
        created_at: datetime,
        episode_count: Optional[int] = None,
        total_runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        production_status: Optional[ProductionStatus] = None,
        budget: Optional[Money] = None,
    ) -> "SeriesSeason":
        return SeriesSeason(
            series_id=series_id, amdb_vote_count=0,
            is_under_inspection=False, created_at=created_at,
            episode_count=episode_count, amdb_rating=None,
            total_runtime=total_runtime, release_date=release_date,
            end_date=end_date, is_ongoing=is_ongoing, genres=genres,
            countries=countries, production_status=production_status,
            budget=budget,
        )

    def update(
        self,
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
        self._update(
            episode_count=episode_count, total_runtime=total_runtime,
            release_date=release_date, end_date=end_date, is_ongoing=is_ongoing,
            genres=genres, countries=countries, production_status=production_status,
            budget=budget,
        )
    
    def add_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_season_exceptions.SeriesSeasonUnderInspection()

        if self.amdb_rating is None:
            self.amdb_rating = sum(votes) / len(votes)
            self.amdb_vote_count = len(votes)
            return

        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) + sum(votes)) /
            (self.amdb_vote_count + len(votes))
        )
        self.amdb_vote_count += len(votes)

    def remove_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_season_exceptions.SeriesSeasonUnderInspection()

        if self.amdb_vote_count == 1:
            self.amdb_rating = None
            self.amdb_vote_count = 0
            return

        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) - sum(votes)) /  # type: ignore
            (self.amdb_vote_count - len(votes))
        )
        self.amdb_vote_count -= len(votes)

    def add_to_inspection(self) -> None:
        self.is_under_inspection = True

    def remove_from_inspection(self) -> None:
        self.is_under_inspection = False