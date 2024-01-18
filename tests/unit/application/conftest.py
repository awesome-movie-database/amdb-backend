import os
from typing import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.sqlalchemy.models.base import Model


TEST_POSTGRES_HOST_ENV = "TEST_POSTGRES_HOST"
TEST_POSTGRES_PORT_ENV = "TEST_POSTGRES_PORT"
TEST_POSTGRES_NAME_ENV = "TEST_POSTGRES_NAME"
TEST_POSTGRES_USER_ENV = "TEST_POSTGRES_USER"
TEST_POSTGRES_PASSWORD_ENV = "TEST_POSTGRES_PASSWORD"


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@pytest.fixture(scope="package")
def postgres_config() -> PostgresConfig:
    return PostgresConfig(
        host=get_env(TEST_POSTGRES_HOST_ENV),
        port=get_env(TEST_POSTGRES_PORT_ENV),
        name=get_env(TEST_POSTGRES_NAME_ENV),
        user=get_env(TEST_POSTGRES_USER_ENV),
        password=get_env(TEST_POSTGRES_PASSWORD_ENV),
    )


@pytest.fixture(scope="package")
def sqlalchemy_engine(postgres_config: PostgresConfig) -> Engine:
    return create_engine(url=postgres_config.dsn)


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
