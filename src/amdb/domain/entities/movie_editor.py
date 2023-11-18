from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class MovieEditor(Entity):

    person_id: UUID
    movie_id: UUID
    created_at: datetime

    @classmethod
    def create(
        cls, person_id: UUID, movie_id: UUID,
        created_at: datetime
    ) -> "MovieEditor":
        return MovieEditor(
            person_id=person_id, movie_id=movie_id,
            created_at=created_at
        )
