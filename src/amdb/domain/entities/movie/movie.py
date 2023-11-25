from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime


@dataclass(slots=True)
class Movie(Entity):
    id: UUID
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
    revenue: Optional[Money]
    mpaa: Optional[MPAA]
    filming_start: Optional[Date]
    filming_end: Optional[Date]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_vote_count: Optional[int]
    kinopoisk_id: Optional[str]
    kinopoisk_rating: Optional[float]
    kinopoisk_vote_count: Optional[int]
