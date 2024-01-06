from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InfrastructureError(Exception):
    """
    Class for Infrastructure errors
    """

    message: str
