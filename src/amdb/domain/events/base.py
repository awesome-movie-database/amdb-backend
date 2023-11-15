from typing import TypeVar


class Event:
    """Base class for Events"""


EventT = TypeVar("EventT", bound=Event)
