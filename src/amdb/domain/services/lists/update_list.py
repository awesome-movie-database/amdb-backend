from datetime import datetime
from typing import Union

from amdb.domain.services.base import Service
from amdb.domain.entities.lists.list import List
from amdb.domain.constants import Unset, unset


class UpdateList(Service):
    def __call__(
        self,
        *,
        list: List,
        updated_at: datetime,
        title: Union[str, Unset] = unset,
        description: Union[str, None, Unset] = unset,
        is_private: Union[bool, Unset] = unset,
    ) -> None:
        self._update_entity(
            entity=list,
            title=title,
            description=description,
            is_private=is_private,
            updated_at=updated_at,
        )
