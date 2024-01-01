import os
from typing import Iterator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from amdb.infrastructure.database.config import DatabaseConfig
from amdb.infrastructure.database.models.base import Model
from amdb.infrastructure.database.builders import build_engine


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
def database_config() -> DatabaseConfig:
    return DatabaseConfig(
        pg_host=get_env(TEST_DATABASE_PG_HOST_ENV),
        pg_port=get_env(TEST_DATABASE_PG_PORT_ENV),
        pg_name=get_env(TEST_DATABASE_PG_NAME_ENV),
        pg_user=get_env(TEST_DATABASE_PG_USER_ENV),
        pg_password=get_env(TEST_DATABASE_PG_PASSWORD_ENV),
    )


@pytest.fixture(scope="package")
def sqlalchemy_engine(database_config: DatabaseConfig) -> Engine:
    return build_engine(database_config)


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
