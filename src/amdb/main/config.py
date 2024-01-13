import os
from dataclasses import dataclass

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig


DATABASE_PG_HOST_ENV = "DATABASE_PG_HOST"
DATABASE_PG_PORT_ENV = "DATABASE_PG_PORT"
DATABASE_PG_NAME_ENV = "DATABASE_PG_NAME"
DATABASE_PG_USER_ENV = "DATABASE_PG_USER"
DATABASE_PG_PASSWORD_ENV = "DATABASE_PG_PASSWORD"


def build_generic_config() -> "GenericConfig":
    database_config = PostgresConfig(
        pg_host=_get_env(DATABASE_PG_HOST_ENV),
        pg_port=_get_env(DATABASE_PG_PORT_ENV),
        pg_name=_get_env(DATABASE_PG_NAME_ENV),
        pg_user=_get_env(DATABASE_PG_USER_ENV),
        pg_password=_get_env(DATABASE_PG_PASSWORD_ENV),
    )
    return GenericConfig(
        database=database_config,
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
