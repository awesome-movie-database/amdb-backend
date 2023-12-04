from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


SeriesId = NewType("SeriesId", UUID)
SeriesTitle = NewType("SeriesTitle", str)


@dataclass(slots=True)
class Series(Entity):
    id: SeriesId
    title: SeriesTitle
    rating: float
    rating_count: int
    genres: list[Genre]
    countries: list[str]
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    end_date: Optional[Date]
    is_ongoing: Optional[bool]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    summary: Optional[str]
    budget: Optional[Money]
    mpaa: Optional[MPAA]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_vote_count: Optional[int]
    kinopoisk_id: Optional[str]
    kinopoisk_rating: Optional[float]
    kinopoisk_vote_count: Optional[int]
