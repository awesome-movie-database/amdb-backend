from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.constants.common import Unset, unset
from amdb.domain.value_objects import Date, Place
from amdb.domain.entities.person.person import Person


class UpdatePerson(Service):
    def __call__(
        self,
        *,
        person: Person,
        timestamp: datetime,
        name: Union[str, Unset] = unset,
        birth_date: Union[Date, None, Unset] = unset,
        birth_place: Union[Place, None, Unset] = unset,
        death_date: Union[Date, None, Unset] = unset,
        death_place: Union[Place, None, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=person,
            name=name,
            birth_date=birth_date,
            birth_place=birth_place,
            death_date=death_date,
            death_place=death_place,
            updated_at=timestamp,
        )
