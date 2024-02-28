from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class UpdateMyProfileCommand:
    email: Optional[str]
