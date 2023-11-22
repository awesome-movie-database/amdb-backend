from dataclasses import dataclass

from .base import DomainException


@dataclass(frozen=True, slots=True)
class RegistrationDenied(DomainException):
    message: str
