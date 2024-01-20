from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: int
    db: int
    password: str
