import os
from typing import Iterator

import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import Session

from amdb.infrastructure.database.models.base import Model


TEST_DATABASE_POSTGRES_USER_ENV = "TEST_DATABASE_POSTGRES_USER"
TEST_DATABASE_POSTGRES_PASSWORD_ENV = "TEST_DATABASE_POSTGRES_PASSWORD"
TEST_DATABASE_POSTGRES_HOST_ENV = "TEST_DATABASE_POSTGRES_HOST"
TEST_DATABASE_POSTGRES_PORT_ENV = "TEST_DATABASE_POSTGRES_PORT"
TEST_DATABASE_POSTGRES_NAME_ENV = "TEST_DATABASE_POSTGRES_NAME"


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@pytest.fixture(scope="session")
def test_sqlalchemy_url() -> str:
    user = get_env(TEST_DATABASE_POSTGRES_USER_ENV)
    password = get_env(TEST_DATABASE_POSTGRES_PASSWORD_ENV)
    host = get_env(TEST_DATABASE_POSTGRES_HOST_ENV)
    port = get_env(TEST_DATABASE_POSTGRES_PORT_ENV)
    name = get_env(TEST_DATABASE_POSTGRES_NAME_ENV)

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@pytest.fixture(scope="session")
def sqlalchemy_engine(test_sqlalchemy_url: str) -> Engine:
    return create_engine(
        url=test_sqlalchemy_url,
    )


@pytest.fixture
def sqlalchemy_session(
    sqlalchemy_engine: Engine,
) -> Iterator[Session]:
    connection = sqlalchemy_engine.connect()
    session = Session(
        bind=sqlalchemy_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    yield session

    session.close()
    connection.close()


@pytest.fixture
def clear_database(
    sqlalchemy_engine: Engine,
) -> None:
    Model.metadata.create_all(
        bind=sqlalchemy_engine,
    )
    yield
    Model.metadata.drop_all(
        bind=sqlalchemy_engine,
    )
