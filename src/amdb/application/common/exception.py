from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    message: str
    extra: Optional[dict] = None
