from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    name: str
    password: str
    email: Optional[str] = None
    telegram: Optional[str] = None
