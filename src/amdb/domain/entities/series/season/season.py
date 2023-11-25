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

    def add_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_season_exceptions.SeriesSeasonUnderInspection()

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
            raise series_season_exceptions.SeriesSeasonUnderInspection()

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
