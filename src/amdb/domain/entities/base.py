from typing import TypeVar


class Entity:
    """Base class for Entities"""


EntityT = TypeVar("EntityT", bound=Entity)
