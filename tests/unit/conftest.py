import os

import pytest
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig


TEST_POSTGRES_HOST_ENV = "TEST_POSTGRES_HOST"
TEST_POSTGRES_PORT_ENV = "TEST_POSTGRES_PORT"
TEST_POSTGRES_NAME_ENV = "TEST_POSTGRES_DB"
TEST_POSTGRES_USER_ENV = "TEST_POSTGRES_USER"
TEST_POSTGRES_PASSWORD_ENV = "TEST_POSTGRES_PASSWORD"

TEST_REDIS_HOST_ENV = "TEST_REDIS_HOST"
TEST_REDIS_PORT_ENV = "TEST_REDIS_PORT"
TEST_REDIS_DB_ENV = "TEST_REDIS_DB"
TEST_REDIS_PASSWORD_ENV = "TEST_REDIS_PASSWORD"


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@pytest.fixture(scope="session")
def postgres_url() -> str:
    postgres_config = PostgresConfig(
        host=_get_env(TEST_POSTGRES_HOST_ENV),
        port=_get_env(TEST_POSTGRES_PORT_ENV),
        name=_get_env(TEST_POSTGRES_NAME_ENV),
        user=_get_env(TEST_POSTGRES_USER_ENV),
        password=_get_env(TEST_POSTGRES_PASSWORD_ENV),
    )
    return postgres_config.dsn


@pytest.fixture(scope="session")
def redis() -> Redis:
    redis = Redis(
        host=_get_env(TEST_REDIS_HOST_ENV),
        port=int(_get_env(TEST_REDIS_PORT_ENV)),
        db=int(_get_env(TEST_REDIS_DB_ENV)),
        password=_get_env(TEST_REDIS_PASSWORD_ENV),
    )
    return redis
