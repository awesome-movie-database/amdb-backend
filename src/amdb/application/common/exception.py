from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    """Base class for Application Errors"""

    message: str
    