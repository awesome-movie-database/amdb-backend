from typing import TypeVar


class Policy:
    """Base class for Policies"""


Policy_T = TypeVar("Policy_T", bound=Policy)
