from dataclasses import dataclass
from enum import IntEnum

from amdb.domain.entities.base import Entity
from .person import PersonId


class RelationType(IntEnum):
    SIBLING = 0
    AUNCLE = 1
    NIBLING = 2
    GRANDPARENT = 3
    GRANDCHILD = 4


@dataclass(slots=True)
class Relation(Entity):
    person_id: PersonId
    relative_id: PersonId
    type: RelationType
