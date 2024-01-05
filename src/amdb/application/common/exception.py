from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    """
    Class for Application errors
    """
    message: str
