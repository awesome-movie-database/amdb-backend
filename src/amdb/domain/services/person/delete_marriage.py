from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person


class DeleteMarriage(Service):
    def __call__(
        self,
        *,
        husband: Person,
        wife: Person,
        children: list[Person],
        timestamp: datetime,
    ) -> None:
        husband.updated_at = timestamp
        wife.updated_at = timestamp

        for child in children:
            child.updated_at = timestamp
