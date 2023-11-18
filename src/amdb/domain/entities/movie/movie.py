from dataclasses import dataclass
from datetime import date, datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset, Genre, MPAA, ProductionStatus
from amdb.domain.value_objects import Money
from amdb.domain.exceptions import movie as movie_exceptions
from amdb.domain.exceptions import vote as vote_exceptions


@dataclass(slots=True)
class Movie(Entity):

    id: UUID
    amdb_vote_count: int
    is_under_inspection: bool
    created_at: datetime

    amdb_rating: Optional[float]
    original_title: Optional[str]
    en_title: Optional[str]
    year: Optional[int]
    runtime: Optional[int]
    release_date: Optional[date]
    genres: Optional[list[Genre]]
    countries: Optional[list[str]]
    production_status: Optional[ProductionStatus]
    description: Optional[str]
    summary: Optional[str]
    budget: Optional[Money]
    revenue: Optional[Money]
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
        created_at: datetime,
        original_title: Optional[str] = None,
        en_title: Optional[str] = None,
        year: Optional[int] = None,
        runtime: Optional[int] = None,
        release_date: Optional[date] = None,
        genres: Optional[list[Genre]] = None,
        countries: Optional[list[str]] = None,
        production_status: Optional[ProductionStatus] = None,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        budget: Optional[Money] = None,
        revenue: Optional[Money] = None,
        mpaa: Optional[MPAA] = None,
        imdb_id: Optional[str] = None,
        imdb_rating: Optional[float] = None,
        imdb_vote_count: Optional[int] = None,
        kinopoisk_id: Optional[str] = None,
        kinopoisk_rating: Optional[float] = None,
        kinopoisk_vote_count: Optional[int] = None,
    ) -> "Movie":
        return Movie(
            id=id, amdb_vote_count=0, is_under_inspection=False,
            created_at=created_at, amdb_rating=None,
            original_title=original_title, en_title=en_title,
            year=year, runtime=runtime, release_date=release_date,
            genres=genres, countries=countries, production_status=production_status,
            description=description, summary=summary, budget=budget,
            revenue=revenue, mpaa=mpaa, imdb_id=imdb_id,
            imdb_rating=imdb_rating, imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id, kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count
        )
    
    def update(
        self,
        original_title: Union[str, None, Type[Unset]] = Unset,
        en_title: Union[str, None, Type[Unset]] = Unset,
        year: Union[int, None, Type[Unset]] = Unset,
        runtime: Union[int, None, Type[Unset]] = Unset,
        release_date: Union[date, None, Type[Unset]] = Unset,
        genres: Union[list[Genre], None, Type[Unset]] = Unset,
        countries: Union[list[str], None, Type[Unset]] = Unset,
        production_status: Union[ProductionStatus, None, Type[Unset]] = Unset,
        description: Union[str, None, Type[Unset]] = Unset,
        summary: Union[str, None, Type[Unset]] = Unset,
        budget: Union[Money, None, Type[Unset]] = Unset,
        revenue: Union[Money, None, Type[Unset]] = Unset,
        mpaa: Union[MPAA, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        imdb_rating: Union[float, None, Type[Unset]] = Unset,
        imdb_vote_count: Union[int, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_rating: Union[float, None, Type[Unset]] = Unset,
        kinopoisk_vote_count: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        self._update(
            original_title=original_title, en_title=en_title, year=year,
            runtime=runtime, release_date=release_date, genres=genres,
            countries=countries, production_status=production_status,
            description=description, summary=summary, budget=budget,
            revenue=revenue, mpaa=mpaa, imdb_id=imdb_id,
            imdb_rating=imdb_rating, imdb_vote_count=imdb_vote_count,
            kinopoisk_id=kinopoisk_id, kinopoisk_rating=kinopoisk_rating,
            kinopoisk_vote_count=kinopoisk_vote_count,
        )
    
    def add_amdb_votes(self, *votes: float) -> None:
        if self.is_under_inspection:
            raise movie_exceptions.MovieUnderInspection()

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
            raise movie_exceptions.MovieUnderInspection()
        
        if self.amdb_rating is None or self.amdb_vote_count < len(votes):
            raise vote_exceptions.NotEnoughAmdbVotes()
        elif self.amdb_vote_count == 1:
            self.amdb_rating = None
            self.amdb_vote_count = 0
            return
        
        self.amdb_rating = (
            ((self.amdb_rating * self.amdb_vote_count) - sum(votes)) /
            (self.amdb_vote_count - len(votes))
        )
        self.amdb_vote_count -= len(votes)
    
    def add_to_inspection(self) -> None:
        if self.is_under_inspection:
            raise movie_exceptions.MovieUnderInspection()
        self.is_under_inspection = True
    
    def remove_from_inspection(self) -> None:
        if not self.is_under_inspection:
            raise movie_exceptions.MovieNotUnderInspection()
        self.is_under_inspection = False
