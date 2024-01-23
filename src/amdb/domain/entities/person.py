from dataclasses import dataclass
from typing import NewType
from uuid import UUID


PersonId = NewType("PersonId", UUID)


@dataclass(frozen=True, slots=True)
class Person:
    id: PersonId
    name: str
