from dataclasses import dataclass
from datetime import date, datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.constants import Unset, Sex
from .base import Entity


@dataclass(slots=True)
class User(Entity):

    id: UUID
    username: str
    password: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    sex: Optional[Sex]
    email: Optional[str]
    country: Optional[str]
    city: Optional[str]
    birth_date: Optional[date]
    updated_at: Optional[datetime]

    @classmethod
    def register(
        cls, id: UUID, username: str, password: str,
        created_at: datetime, sex: Optional[Sex] = None,
        email: Optional[str] = None, country: Optional[str] = None,
        city: Optional[str] = None, birth_date: Optional[date] = None,
    ) -> "User":
        return User(
            id=id, username=username, password=password,
            is_active=True, is_verified=False, created_at=created_at,
            sex=sex, email=email, country=country, city=city,
            birth_date=birth_date, updated_at=None,
        )

    def update(
        self,
        updated_at: datetime,
        username: Union[str, Type[Unset]] = Unset,
        password: Union[str, Type[Unset]] = Unset,
        sex: Union[Sex, None, Type[Unset]] = Unset,
        email: Union[str, None, Type[Unset]] = Unset,
        country: Union[str, None, Type[Unset]] = Unset,
        city: Union[str, None, Type[Unset]] = Unset,
        birth_date: Union[date, None, Type[Unset]] = Unset,
    ) -> None:
        self._update_fields(
            username=username, password=password, sex=sex, email=email,
            country=country, city=city, birth_date=birth_date,
        )
        self.updated_at = updated_at
    
    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
    
    def verify(self) -> None:
        self.is_verified = True
