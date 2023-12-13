from dataclasses import dataclass
from datetime import date
from typing import Optional

from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Place


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    name: str
    password: str
    email: Optional[str] = None
    sex: Optional[Sex] = None
    birth_date: Optional[date] = None
    location: Optional[Place] = None
