from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money
from .series import SeriesId


@dataclass(slots=True)
class SeriesEpisode(Entity):
    series_id: SeriesId
    season_number: int
    number: int
    rating: float
    rating_count: int
    genres: list[Genre]
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    budget: Optional[Money]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_rating_count: Optional[int]
    updated_at: Optional[datetime]
