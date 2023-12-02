from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Date:
    year: int

    month: Optional[int]
    day: Optional[int]


@dataclass(frozen=True, slots=True)
class Place:
    country: str

    state: Optional[str]
    city: Optional[str]
