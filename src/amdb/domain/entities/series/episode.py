from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.person.person import PersonId
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
    director_ids: list[PersonId]
    art_director_ids: list[PersonId]
    casting_director_ids: list[PersonId]
    composer_ids: list[PersonId]
    operator_ids: list[PersonId]
    producer_ids: list[PersonId]
    editor_ids: list[PersonId]
    screenwriter_ids: list[PersonId]
    created_at: datetime

    runtime: Optional[Runtime]
    release_date: Optional[Date]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    budget: Optional[Money]
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    imdb_vote_count: Optional[int]
    updated_at: Optional[datetime]
