from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    name: str
    email: Optional[str]
    password: str
