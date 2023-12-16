from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from amdb.domain.entities.base import Entity
from amdb.domain.value_objects import Date
from .person import PersonId


class MarriageStatus(IntEnum):
    MARRIAGE = 0
    DIVORCE = 1
    HIS_DEATH = 2
    HER_DEATH = 3
    HE_FILED_FOR_DIVORCE = 4
    SHE_FILED_FOR_DIVORCED = 5


@dataclass(slots=True)
class Marriage(Entity):
    husband_id: PersonId
    wife_id: PersonId
    child_ids: list[PersonId]
    status: MarriageStatus

    start_date: Optional[Date]
    end_date: Optional[Date]
