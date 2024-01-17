from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginQuery:
    name: str
    password: str
