from typing import TypeVar


class Service:
    """Base class for Services"""


Service_T = TypeVar("Service_T", bound=Service)
