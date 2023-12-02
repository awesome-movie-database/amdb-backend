from typing import TypeVar


class Entity:
    """Base class for Entities"""


Entity_T = TypeVar("Entity_T", bound=Entity)
