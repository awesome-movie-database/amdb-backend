from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.constants.common import Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money
from .series import SeriesId


@dataclass(slots=True)
class SeriesSeasonGenre:
    genre: Genre
    episode_count: int


@dataclass(slots=True)
class SeriesSeason(Entity):
    series_id: SeriesId
    number: int
    rating: float
    rating_count: int
    genres: list[SeriesSeasonGenre]
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    end_date: Optional[Date]
    is_ongoing: Optional[bool]
    production_status: Optional[ProductionStatus]
    budget: Optional[Money]
    updated_at: Optional[datetime]
