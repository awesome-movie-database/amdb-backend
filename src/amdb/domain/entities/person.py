from dataclasses import dataclass
from datetime import date, datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.constants import Unset, Sex
from .base import Entity


@dataclass(frozen=True, slots=True)
class PersonName:
    en_name: Optional[str]
    original_name: Optional[str]

    def __post_init__(self) -> None:
        if self.en_name is None and self.original_name is None:
            raise ValueError(
                "Name must at least include en_name or original_name",
            )


@dataclass(slots=True)
class Person(Entity):
    id: UUID
    name: PersonName
    is_under_inspection: bool
    created_at: datetime

    sex: Optional[Sex]
    birth_date: Optional[date]
    birth_place: Optional[str]
    imdb_id: Optional[str]
    kinopoisk_id: Optional[str]

    @classmethod
    def create(
        cls,
        id: UUID,
        name: PersonName,
        created_at: datetime,
        sex: Optional[Sex] = None,
        birth_date: Optional[date] = None,
        birth_place: Optional[str] = None,
        imdb_id: Optional[str] = None,
        kinopoisk_id: Optional[str] = None,
    ) -> "Person":
        return Person(
            id=id,
            name=name,
            is_under_inspection=False,
            created_at=created_at,
            sex=sex,
            birth_date=birth_date,
            birth_place=birth_place,
            imdb_id=imdb_id,
            kinopoisk_id=kinopoisk_id,
        )

    def update(
        self,
        name: Union[PersonName, None, Type[Unset]] = Unset,
        sex: Union[Sex, None, Type[Unset]] = Unset,
        birth_date: Union[date, None, Type[Unset]] = Unset,
        birth_place: Union[str, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
    ) -> None:
        self._update(
            name=name,
            sex=sex,
            birth_date=birth_date,
            birth_place=birth_place,
            imdb_id=imdb_id,
            kinopoisk_id=kinopoisk_id,
        )

    def add_to_inspection(self) -> None:
        self.is_under_inspection = True

    def remove_from_inspection(self) -> None:
        self.is_under_inspection = False
