from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    """
    Class for Domain errors
    """

    message: str
