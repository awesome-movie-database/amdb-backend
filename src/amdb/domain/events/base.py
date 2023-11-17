from typing import TypeVar


class Event:
    """Base class for Events"""


Event_T = TypeVar("Event_T", bound=Event)
