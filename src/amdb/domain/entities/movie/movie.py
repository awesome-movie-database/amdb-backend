from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset, Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime
from amdb.domain.exceptions import movie as movie_exceptions


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

    def remove_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise movie_exceptions.MovieUnderInspection()

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
