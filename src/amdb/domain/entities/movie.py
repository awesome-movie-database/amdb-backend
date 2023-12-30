from dataclasses import dataclass
from typing import NewType
from uuid import UUID


MovieId = NewType("MovieId", UUID)


@dataclass(slots=True)
class Movie:
    id: MovieId
    title: str
    rating: float
    rating_count: int
