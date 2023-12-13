from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Place


UserId = NewType("UserId", UUID)


@dataclass(slots=True)
class User(Entity):
    id: UserId
    name: str
    password: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    email: Optional[str]
    sex: Optional[Sex]
    birth_date: Optional[date]
    location: Optional[Place]
    verified_at: Optional[datetime]
    updated_at: Optional[datetime]
