from dataclasses import dataclass
from typing import Union

from amdb.domain.unset import UNSET_T, UNSET


@dataclass(frozen=True, slots=True)
class UpdateMyProfileCommand:
    email: Union[str, None, UNSET_T] = UNSET
    telegram: Union[str, None, UNSET_T] = UNSET
