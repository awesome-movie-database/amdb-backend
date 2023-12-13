from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    messsage: str
