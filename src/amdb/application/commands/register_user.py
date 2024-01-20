from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    name: str
    password: str
