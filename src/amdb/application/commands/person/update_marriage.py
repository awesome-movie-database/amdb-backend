from dataclasses import dataclass
from typing import Union

from amdb.domain.entities.person.person import PersonId
from amdb.domain.entities.person.marriage import MarriageId, MarriageStatus
from amdb.domain.constants.common import Unset, unset
from amdb.domain.value_objects import Date


@dataclass(frozen=True, slots=True)
class UpdateMarriageCommand:
    marriage_id: MarriageId
    child_ids: Union[list[PersonId], Unset] = unset
    status: Union[MarriageStatus, Unset] = unset
    start_date: Union[Date, None, Unset] = unset
    end_date: Union[Date, None, Unset] = unset
