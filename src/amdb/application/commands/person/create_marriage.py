from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.marriage import MarriageStatus
from amdb.domain.value_objects import Date


@dataclass(frozen=True, slots=True)
class CreateMarriageCommand:
    husband_id: PersonId
    wife_id: PersonId
    child_ids: list[PersonId]
    status: MarriageStatus
    start_date: Optional[Date] = None
    end_date: Optional[Date] = None
