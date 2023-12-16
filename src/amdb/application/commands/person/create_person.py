from dataclasses import dataclass
from typing import Optional

from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place


@dataclass(frozen=True, slots=True)
class CreatePersonCommand:
    name: str
    sex: Optional[Sex] = None
    birth_date: Optional[Date] = None
    birth_place: Optional[Place] = None
    death_date: Optional[Date] = None
    death_place: Optional[Place] = None
