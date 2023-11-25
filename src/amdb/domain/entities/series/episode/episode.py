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

    def add_to_inspection(self) -> None:
        self.is_under_inspection = True

    def remove_from_inspection(self) -> None:
        self.is_under_inspection = False
