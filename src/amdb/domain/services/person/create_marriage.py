from datetime import datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.value_objects import Date
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import Marriage, MarriageStatus


class CreateMarriage(Service):
    def __call__(
        self,
        *,
        husband: Person,
        wife: Person,
        children: list[Person],
        status: MarriageStatus,
        timestamp: datetime,
        start_date: Optional[Date] = None,
        end_date: Optional[Date] = None,
    ) -> Marriage:
        husband.updated_at = timestamp
        wife.updated_at = timestamp

        child_ids = []
        for child in children:
            child_ids.append(child.id)
            child.updated_at = timestamp

        return Marriage(
            husband_id=husband.id,
            wife_id=wife.id,
            child_ids=child_ids,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
