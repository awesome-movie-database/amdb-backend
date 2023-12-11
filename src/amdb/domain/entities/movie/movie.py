from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


MovieId = NewType("MovieId", UUID)


@dataclass(slots=True)
class Movie(Entity):
    id: MovieId
    title: str
    rating: float
    rating_count: int
    genres: list[Genre]
    countries: list[str]
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    summary: Optional[str]
    budget: Optional[Money]
    revenue: Optional[Money]
    mpaa: Optional[MPAA]
    filming_start: Optional[Date]
    filming_end: Optional[Date]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_rating_count: Optional[int]
    kinopoisk_id: Optional[str]
    kinopoisk_rating: Optional[float]
    kinopoisk_rating_count: Optional[int]
    updated_at: Optional[datetime]
