from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    messsage: str
    extra: Optional[dict] = None
