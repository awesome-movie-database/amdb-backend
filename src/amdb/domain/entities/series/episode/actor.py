from dataclasses import dataclass
from datetime import datetime
from typing import Type, Optional, Union
from uuid import UUID

from amdb.domain.entities.base import Entity
from amdb.domain.constants import Unset


@dataclass(slots=True)
class SeriesEpisodeActor(Entity):
    person_id: UUID
    series_id: UUID
    episode: int
    role: str
    created_at: datetime

    top_cast_number: Optional[int]

    @classmethod
    def create(
        cls,
        person_id: UUID,
        series_id: UUID,
        episode: int,
        role: str,
        created_at: datetime,
        top_cast_number: int,
    ) -> "SeriesEpisodeActor":
        return SeriesEpisodeActor(
            person_id=person_id,
            series_id=series_id,
            episode=episode,
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
