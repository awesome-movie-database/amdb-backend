from dataclasses import dataclass
from datetime import date
from typing import NewType
from uuid import UUID


MovieId = NewType("MovieId", UUID)


@dataclass(slots=True)
class Movie:
    id: MovieId
    title: str
    release_date: date
    rating: float
    rating_count: int
