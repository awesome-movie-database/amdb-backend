from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.entities.person.person import PersonId
from amdb.domain.constants import Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Date, Runtime, Money


MovieId = NewType("MovieId", UUID)
MovieTitle = NewType("MovieTitle", str)


@dataclass(slots=True)
class Movie(Entity):
    id: MovieId
    title: MovieTitle
    rating: float
    rating_count: int
    genres: list[Genre]
    countries: list[str]
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
    updated_at: Optional[datetime]
