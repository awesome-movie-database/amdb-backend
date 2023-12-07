from typing import Union, TypeVar, Any

from amdb.domain.constants import Unset, unset
from amdb.domain.entities.base import Entity_T


class Service:
    """Base class for Services"""

    def _update_entity(self, entity: Entity_T, **changes: Union[Any, Unset]) -> None:
        """
        Updates `entity` fields where `changes` values
        are not `Unset`.
        """
        for name, value in changes.items():
            if value is unset:
                continue
            setattr(entity, name, value)


Service_T = TypeVar("Service_T", bound=Service)
