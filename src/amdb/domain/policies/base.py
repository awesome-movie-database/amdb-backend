from typing import TypeVar


class Policy:
    """Base class for Policies"""


PolicyT = TypeVar("PolicyT", bound=Policy)
