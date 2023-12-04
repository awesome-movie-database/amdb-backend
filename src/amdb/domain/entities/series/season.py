from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Genre, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money
from .series import SeriesId


@dataclass(slots=True)
class SeriesSeason(Entity):
    series_id: SeriesId
    rating: float
    rating_count: int
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    end_date: Optional[Date]
    is_ongoing: Optional[bool]
    genres: Optional[list[Genre]]
    countries: Optional[list[str]]
    production_status: Optional[ProductionStatus]
    budget: Optional[Money]
