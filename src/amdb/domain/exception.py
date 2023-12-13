from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    message: str
