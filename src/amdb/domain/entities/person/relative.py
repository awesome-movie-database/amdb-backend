from dataclasses import dataclass
from enum import IntEnum

from .person import PersonId


class RelativeType(IntEnum):
    SIBLING = 0
    AUNT_OR_UNCLE = 1
    NIECE_OR_NEPHEW = 2
    GRANDMOTHER_OR_GRANDFATHER = 3


@dataclass(slots=True)
class Relative:
    person_id: PersonId
    relative_id: PersonId
    type: RelativeType
