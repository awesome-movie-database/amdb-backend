from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class SessionIdentityProviderConfig:
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    session_lifetime: timedelta
