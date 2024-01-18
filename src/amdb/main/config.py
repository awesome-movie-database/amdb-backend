import os
from dataclasses import dataclass

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig


POSTGRES_HOST_ENV = "POSTGRES_HOST"
POSTGRES_PORT_ENV = "POSTGRES_PORT"
POSTGRES_NAME_ENV = "POSTGRES_NAME"
POSTGRES_USER_ENV = "POSTGRES_USER"
POSTGRES_PASSWORD_ENV = "POSTGRES_PASSWORD"


def build_generic_config() -> "GenericConfig":
    postgres_config = PostgresConfig(
        host=_get_env(POSTGRES_HOST_ENV),
        port=_get_env(POSTGRES_PORT_ENV),
        name=_get_env(POSTGRES_NAME_ENV),
        user=_get_env(POSTGRES_USER_ENV),
        password=_get_env(POSTGRES_PASSWORD_ENV),
    )
    return GenericConfig(
        postgres=postgres_config,
    )


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@dataclass(frozen=True, slots=True)
class GenericConfig:
    postgres: PostgresConfig
