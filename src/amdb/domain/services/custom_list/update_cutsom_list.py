from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.custom_list.custom_list import CustomList
from amdb.domain.constants import Unset, unset


class UpdateCustomList(Service):
    def __call__(
        self,
        *,
        custom_list: CustomList,
        updated_at: datetime,
        title: Union[str, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        is_private: Union[bool, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=custom_list,
            title=title,
            description=description,
            is_private=is_private,
            updated_at=updated_at,
        )
