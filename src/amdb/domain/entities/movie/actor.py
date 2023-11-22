from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset


@dataclass(slots=True)
class MovieActor(Entity):
    person_id: UUID
    movie_id: UUID
    role: str
    created_at: datetime

    top_cast_number: Optional[int]

    @classmethod
    def create(
        cls,
        person_id: UUID,
        movie_id: UUID,
        role: str,
        created_at: datetime,
        top_cast_number: int,
    ) -> "MovieActor":
        return MovieActor(
            person_id=person_id,
            movie_id=movie_id,
            role=role,
            created_at=created_at,
            top_cast_number=top_cast_number,
        )

    def update(
        self,
        role: Union[str, Type[Unset]] = Unset,
        top_cast_number: Union[int, None, Type[Unset]] = Unset,
    ) -> None:
        self._update(
            role=role,
            top_cast_number=top_cast_number,
        )
