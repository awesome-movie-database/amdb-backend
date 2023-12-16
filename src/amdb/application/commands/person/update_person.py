from dataclasses import dataclass
from typing import Union

from amdb.domain.entities.person.person import PersonId
from amdb.domain.constants.common import Unset, unset, Sex
from amdb.domain.value_objects import Date, Place


@dataclass(frozen=True, slots=True)
class UpdatePersonCommand:
    person_id: PersonId
    name: Union[str, Unset] = unset
    sex: Union[Sex, None, Unset] = unset
    birth_date: Union[Date, None, Unset] = unset
    birth_place: Union[Place, None, Unset] = unset
    death_date: Union[Date, None, Unset] = unset
    death_place: Union[Place, None, Unset] = unset
