from dataclasses import dataclass
from datetime import date
from typing import Union

from amdb.domain.constants.common import Unset, unset, Sex
from amdb.domain.value_objects import Place


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    name: Union[str, Unset] = unset
    password: Union[str, Unset] = unset
    email: Union[str, None, Unset] = unset
    sex: Union[Sex, None, Unset] = unset
    birth_date: Union[date, None, Unset] = unset
    location: Union[Place, None, Unset] = unset
