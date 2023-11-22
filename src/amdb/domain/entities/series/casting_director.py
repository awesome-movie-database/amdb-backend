from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from amdb.domain.entities.base import Entity


@dataclass(slots=True)
class SeriesEpisodeCastingDirector(Entity):
    person_id: UUID
    series_id: UUID
    episode: int
    created_at: datetime

    @classmethod
    def create(
        cls,
        person_id: UUID,
        series_id: UUID,
        episode: int,
        created_at: datetime,
    ) -> "SeriesEpisodeCastingDirector":
        return SeriesEpisodeCastingDirector(
            person_id=person_id,
            series_id=series_id,
            episode=episode,
            created_at=created_at,
        )
