from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.relative import RelativeType, Relative


class CreateRelative(Service):
    def __call__(
        self,
        person: Person,
        relative: Person,
        type: RelativeType,
        created_at: datetime,
    ) -> Relative:
        person.updated_at = created_at
        relative.updated_at = created_at

        return Relative(
            person_id=person.id,
            relative_id=relative.id,
            type=type,
        )
