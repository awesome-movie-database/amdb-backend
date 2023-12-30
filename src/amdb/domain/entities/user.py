from dataclasses import dataclass
from typing import NewType
from uuid import UUID


UserId = NewType("UserId", UUID)


@dataclass(slots=True)
class User:
    id: UserId
    name: str
