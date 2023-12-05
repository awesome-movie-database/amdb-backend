from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.entities.person.person import PersonId
from .series import SeriesId


@dataclass(slots=True)
class SeriesActor(Entity):
    series_id: SeriesId
    season_number: int
    episode_number: int
    person_id: PersonId

    role: Optional[str]
    is_star: Optional[bool]
