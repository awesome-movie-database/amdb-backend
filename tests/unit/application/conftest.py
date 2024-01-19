import os
from typing import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.sqlalchemy.models.base import Model


TEST_POSTGRES_HOST_ENV = "TEST_POSTGRES_HOST"
TEST_POSTGRES_PORT_ENV = "TEST_POSTGRES_PORT"
TEST_POSTGRES_NAME_ENV = "TEST_POSTGRES_NAME"
TEST_POSTGRES_USER_ENV = "TEST_POSTGRES_USER"
TEST_POSTGRES_PASSWORD_ENV = "TEST_POSTGRES_PASSWORD"

TEST_REDIS_HOST_ENV = "TEST_REDIS_HOST"
TEST_REDIS_PORT_ENV = "TEST_REDIS_PORT"
TEST_REDIS_DB_ENV = "TEST_REDIS_DB"


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@pytest.fixture(scope="package")
def sqlalchemy_engine() -> Engine:
    postgres_config = PostgresConfig(
        host=_get_env(TEST_POSTGRES_HOST_ENV),
        port=_get_env(TEST_POSTGRES_PORT_ENV),
        name=_get_env(TEST_POSTGRES_NAME_ENV),
        user=_get_env(TEST_POSTGRES_USER_ENV),
        password=_get_env(TEST_POSTGRES_PASSWORD_ENV),
    )
    return create_engine(url=postgres_config.dsn)


@pytest.fixture(scope="package")
def redis() -> Redis:
    redis = Redis(
        host=_get_env(TEST_REDIS_HOST_ENV),
        port=int(_get_env(TEST_REDIS_PORT_ENV)),
        db=int(_get_env(TEST_REDIS_DB_ENV)),
    )
    return redis


@pytest.fixture(autouse=True)
def clear_database(sqlalchemy_engine: Engine) -> Iterator[None]:
    Model.metadata.create_all(sqlalchemy_engine)
    yield
    Model.metadata.drop_all(sqlalchemy_engine)


@pytest.fixture
def sqlalchemy_session(sqlalchemy_engine: Engine) -> Iterator[Session]:
    connection = sqlalchemy_engine.connect()
    session = Session(connection, expire_on_commit=False)

    yield session

    session.close()
    connection.close()
