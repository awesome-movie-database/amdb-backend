from dataclasses import dataclass
from datetime import date, datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.constants import Unset, Sex
from amdb.domain.exceptions import person as person_exceptions
from .base import Entity


@dataclass(slots=True)
class Person(Entity):

    id: UUID
    is_under_inspection: bool
    created_at: datetime

    original_name: Optional[str]
    en_name: Optional[str]
    sex: Optional[Sex]
    birth_date: Optional[date]
    birth_place: Optional[str]
    imdb_id: Optional[str]
    kinopoisk_id: Optional[str]

    @classmethod
    def create(
        cls,
        id: UUID,
        created_at: datetime,
        original_name: Optional[str] = None,
        en_name: Optional[str] = None,
        sex: Optional[Sex] = None,
        birth_date: Optional[date] = None,
        birth_place: Optional[str] = None,
        imdb_id: Optional[str] = None,
        kinopoisk_id: Optional[str] = None,
    ) -> "Person":
        return Person(
            id=id, is_under_inspection=False, created_at=created_at,
            original_name=original_name, en_name=en_name, sex=sex,
            birth_date=birth_date, birth_place=birth_place,
            imdb_id=imdb_id, kinopoisk_id=kinopoisk_id,
        )
    
    def update(
        self,
        original_name: Union[str, None, Type[Unset]] = Unset,
        en_name: Union[str, None, Type[Unset]] = Unset,
        sex: Union[Sex, None, Type[Unset]] = Unset,
        birth_date: Union[date, None, Type[Unset]] = Unset,
        birth_place: Union[str, None, Type[Unset]] = Unset,
        imdb_id: Union[str, None, Type[Unset]] = Unset,
        kinopoisk_id: Union[str, None, Type[Unset]] = Unset,
    ) -> "Person":
        self._update(
            original_name=original_name, en_name=en_name, sex=sex,
            birth_date=birth_date, birth_place=birth_place,
            imdb_id=imdb_id, kinopoisk_id=kinopoisk_id
        )

    def add_to_inspection(self) -> None:
        if self.is_under_inspection:
            raise person_exceptions.PersonUnderInspection()
        self.is_under_inspection = True
    
    def remove_from_inspection(self) -> None:
        if not self.is_under_inspection:
            raise person_exceptions.PersonNotUnderInspection()
        self.is_under_inspection = False