from dataclasses import dataclass
from typing import NewType, Optional
from uuid import UUID


UserId = NewType("UserId", UUID)


@dataclass(slots=True)
class User:
    id: UserId
    name: str
    email: Optional[str]
