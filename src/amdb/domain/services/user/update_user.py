from datetime import date, datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import UserName, User
from amdb.domain.constants import Unset, unset, Sex
from amdb.domain.value_objects import Place


class UpdateUser(Service):
    def __call__(
        self,
        *,
        user: User,
        timestamp: datetime,
        name: Union[UserName, Unset] = unset,
        password: Union[str, Unset] = unset,
        sex: Union[Sex, None, Unset] = unset,
        birth_date: Union[date, None, Unset] = unset,
        location: Union[Place, None, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=user,
            name=name,
            password=password,
            sex=sex,
            birth_date=birth_date,
            location=location,
            updated_at=timestamp,
        )
