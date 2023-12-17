from dataclasses import dataclass
from typing import Optional

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.relation import RelativeType
from amdb.domain.entities.person.marriage import MarriageStatus
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place


@dataclass(frozen=True, slots=True)
class RelationData:
    person_id: PersonId
    type: RelativeType


@dataclass(frozen=True, slots=True)
class MarriageData:
    person_id: PersonId
    status: MarriageStatus
    child_ids: list[PersonId]
    start_date: Optional[Date] = None
    end_date: Optional[Date] = None


@dataclass(frozen=True, slots=True)
class CreatePersonCommand:
    name: str
    sex: Sex
    birth_date: Optional[Date] = None
    birth_place: Optional[Place] = None
    death_date: Optional[Date] = None
    death_place: Optional[Place] = None
    relations_data: Optional[list[RelationData]] = None
    marriages_data: Optional[list[MarriageData]] = None
