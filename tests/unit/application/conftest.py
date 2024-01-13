import os
from typing import Iterator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.sqlalchemy.models.base import Model
from amdb.infrastructure.persistence.sqlalchemy.builders import build_engine


TEST_DATABASE_PG_HOST_ENV = "TEST_DATABASE_PG_HOST"
TEST_DATABASE_PG_PORT_ENV = "TEST_DATABASE_PG_PORT"
TEST_DATABASE_PG_NAME_ENV = "TEST_DATABASE_PG_NAME"
TEST_DATABASE_PG_USER_ENV = "TEST_DATABASE_PG_USER"
TEST_DATABASE_PG_PASSWORD_ENV = "TEST_DATABASE_PG_PASSWORD"


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@pytest.fixture(scope="package")
def postgres_config() -> PostgresConfig:
    return PostgresConfig(
        host=get_env(TEST_DATABASE_PG_HOST_ENV),
        port=get_env(TEST_DATABASE_PG_PORT_ENV),
        name=get_env(TEST_DATABASE_PG_NAME_ENV),
        user=get_env(TEST_DATABASE_PG_USER_ENV),
        password=get_env(TEST_DATABASE_PG_PASSWORD_ENV),
    )


@pytest.fixture(scope="package")
def sqlalchemy_engine(postgres_config: PostgresConfig) -> Engine:
    return build_engine(postgres_config)


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
