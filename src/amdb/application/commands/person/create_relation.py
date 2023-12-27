from dataclasses import dataclass

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.relation import RelationType


@dataclass(frozen=True, slots=True)
class CreateRelationCommand:
    person_id: PersonId
    relative_id: PersonId
    type: RelationType
