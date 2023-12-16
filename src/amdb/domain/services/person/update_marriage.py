from dataclasses import dataclass
from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.constants.common import Unset, unset
from amdb.domain.value_objects import Date
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import MarriageStatus, Marriage


@dataclass(frozen=True, slots=True)
class Children:
    old_children: list[Person]
    new_children: list[Person]


class UpdateMarriage(Service):
    def __call__(
        self,
        *,
        marriage: Marriage,
        husband: Person,
        wife: Person,
        timestamp: datetime,
        children: Union[Children, Unset] = unset,
        status: Union[MarriageStatus, Unset] = unset,
        start_date: Union[Date, None, Unset] = unset,
        end_date: Union[Date, None, Unset] = unset,
    ) -> None:
        husband.updated_at = timestamp
        wife.updated_at = timestamp

        if children is not unset:
            child_ids = [child.id for child in children.new_children]
            self._update_children(
                old_children=children.old_children,
                new_children=children.new_children,
                updated_at=timestamp,
            )
        else:
            child_ids = marriage.child_ids

        self._update_entity(
            entity=marriage,
            child_ids=child_ids,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )

    def _update_children(
        self,
        *,
        old_children: list[Person],
        new_children: list[Person],
        updated_at: datetime,
    ) -> None:
        for old_child in old_children:
            if old_child in new_children:
                continue
            old_child.updated_at = updated_at

        for new_child in new_children:
            if new_child in old_children:
                continue
            new_child.updated_at = updated_at
