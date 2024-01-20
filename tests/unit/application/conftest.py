import os
from typing import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.sqlalchemy.models.base import Model
from amdb.infrastructure.persistence.sqlalchemy.gateways.user import SQLAlchemyUserGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.movie import SQLAlchemyMovieGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.rating import SQLAlchemyRatingGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.user_password_hash import (
    SQLAlchemyUserPasswordHashGateway,
)
from amdb.infrastructure.persistence.redis.gateways.permissions import RedisPermissionsGateway
from amdb.infrastructure.persistence.sqlalchemy.mappers.user import UserMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.movie import MovieMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.rating import RatingMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.user_password_hash import (
    UserPasswordHashMapper,
)
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.password_manager.password_manager import HashingPasswordManager


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
        password=_get_env(TEST_REDIS_PASSWORD_ENV),
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


@pytest.fixture
def permissions_gateway(redis: Redis) -> RedisPermissionsGateway:
    return RedisPermissionsGateway(redis)


@pytest.fixture
def user_gateway(sqlalchemy_session: Session) -> SQLAlchemyUserGateway:
    return SQLAlchemyUserGateway(sqlalchemy_session, UserMapper())


@pytest.fixture
def movie_gateway(sqlalchemy_session: Session) -> SQLAlchemyMovieGateway:
    return SQLAlchemyMovieGateway(sqlalchemy_session, MovieMapper())


@pytest.fixture
def rating_gateway(sqlalchemy_session: Session) -> SQLAlchemyRatingGateway:
    return SQLAlchemyRatingGateway(sqlalchemy_session, RatingMapper())


@pytest.fixture
def password_manager(sqlalchemy_session: Session) -> HashingPasswordManager:
    user_password_hash_gateway = SQLAlchemyUserPasswordHashGateway(
        session=sqlalchemy_session,
        mapper=UserPasswordHashMapper(),
    )
    return HashingPasswordManager(
        hasher=Hasher(),
        user_password_hash_gateway=user_password_hash_gateway,
    )


@pytest.fixture
def unit_of_work(sqlalchemy_session: Session) -> Session:
    return sqlalchemy_session
