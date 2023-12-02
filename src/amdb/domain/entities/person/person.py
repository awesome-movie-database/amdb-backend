from dataclasses import dataclass
from typing import Optional, NewType
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Sex
from amdb.domain.value_objects import Date, Place


PersonId = NewType("PersonId", UUID)
PersonName = NewType("PersonName", str)


@dataclass(slots=True)
class Person(Entity):
    id: PersonId
    name: PersonName

    sex: Optional[Sex]
    birth_date: Optional[Date]
    birth_place: Optional[Place]
    death_date: Optional[Date]
    death_place: Optional[Place]
