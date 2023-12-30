from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    name: str
