from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset, Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Money, Date, Title, Runtime
from amdb.domain.exceptions import series as series_exceptions


@dataclass(slots=True)
class Series(Entity):

    id: UUID
    title: Title
    amdb_vote_count: int
    is_under_inspection: bool
    created_at: datetime

    season_count: Optional[int]
    episode_count: Optional[int]
    amdb_rating: Optional[float]
    total_runtime: Optional[Runtime]
    release_date: Optional[Date]
    end_date: Optional[Date]
    is_ongoing: Optional[bool]
    genres: Optional[list[Genre]]
    countries: Optional[list[str]]
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

    @classmethod
    def create(
        cls,
        id: UUID,
        title: Title,
        created_at: datetime,
        season_count: Optional[int] = None,
        episode_count: Optional[int] = None,
        total_runtime: Optional[Runtime] = None,
        release_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
        is_ongoing: Optional[bool] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_vote_count: Optional[int] = None,
    ) -> "Series":
        return Series(
            id=id, title=title, amdb_vote_count=0,
            is_under_inspection=False, created_at=created_at,
            season_count=season_count, episode_count=episode_count,
            amdb_rating=None, total_runtime=total_runtime,
            release_date=release_date, end_date=end_date,
            is_ongoing=is_ongoing, genres=genres, countries=countries,
            production_status=production_status, description=description,
            summary=summary, budget=budget, mpaa=mpaa, imdb_id=imdb_id,
            imdb_rating=imdb_rating, imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id, kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
        )

    def update(
        self,
        title: Union[Title, Type[Unset]] = Unset,
        season_count: Union[int, None, Type[Unset]] = Unset,
        episode_count: Union[int, None, Type[Unset]] = Unset,
        total_runtime: Union[Runtime, None, Type[Unset]] = Unset,
        release_date: Union[Date, None, Type[Unset]] = Unset,
        end_date: Union[Date, None, Type[Unset]] = Unset,
        is_ongoing: Union[bool, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        description: Union[str, None, Type[Unset]] = Unset,
        summary: Union[str, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
        mpaa: Union[MPAA, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        imdb_rating: Union[float, None, Type[Unset]] = Unset,
        imdb_vote_count: Union[int, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_rating: Union[float, None, Type[Unset]] = Unset,
        kinopoisk_vote_count: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        self._update(
            title=title, season_count=season_count, episode_count=episode_count,
            total_runtime=total_runtime, release_date=release_date, end_date=end_date,
            is_ongoing=is_ongoing, genres=genres, countries=countries,
            production_status=production_status, description=description, summary=summary,
            budget=budget, mpaa=mpaa, imdb_id=imdb_id, imdb_rating=imdb_rating,
            imdb_vote_count=imdb_vote_count, kinopoisk_id=kinopoisk_id,
            kinopoisk_rating=kinopoisk_rating, kinopoisk_vote_count=kinopoisk_vote_count,
        )

    def add_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_exceptions.SeriesUnderInspection()

        if self.amdb_rating is None:
            self.amdb_rating = sum(votes) / len(votes)
            self.amdb_vote_count = len(votes)
            return

        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) + sum(votes)) /
            (self.amdb_vote_count + len(votes))
        )
        self.amdb_vote_count += len(votes)

    def remove_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise series_exceptions.SeriesNotUnderInspection()

        if self.amdb_vote_count == 1:
            self.amdb_rating = None
            self.amdb_vote_count = 0
            return

        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) - sum(votes)) /  # type: ignore
            (self.amdb_vote_count - len(votes))
        )
        self.amdb_vote_count -= len(votes)

    def add_to_inspection(self) -> None:
        self.is_under_inspection = True

    def remove_from_inspection(self) -> None:
        self.is_under_inspection = False
