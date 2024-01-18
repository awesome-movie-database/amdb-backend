from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class SessionConfig:
    session_lifetime: timedelta
