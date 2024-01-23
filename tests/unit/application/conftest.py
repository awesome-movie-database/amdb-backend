from typing import Iterator
from unittest.mock import Mock

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.models.base import Model
from amdb.infrastructure.persistence.sqlalchemy.gateways.user import SQLAlchemyUserGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.person import SQLAlchemyPersonGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.movie import SQLAlchemyMovieGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.rating import SQLAlchemyRatingGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.user_password_hash import (
    SQLAlchemyUserPasswordHashGateway,
)
from amdb.infrastructure.persistence.redis.gateways.permissions import RedisPermissionsGateway
from amdb.infrastructure.persistence.sqlalchemy.mappers.user import UserMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.person import PersonMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.movie import MovieMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.rating import RatingMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.user_password_hash import (
    UserPasswordHashMapper,
)
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.password_manager.password_manager import HashingPasswordManager


@pytest.fixture(scope="package")
def sqlalchemy_engine(postgres_url: str) -> Engine:
    return create_engine(url=postgres_url)


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
def person_gateway(sqlalchemy_session: Session) -> SQLAlchemyPersonGateway:
    return SQLAlchemyPersonGateway(sqlalchemy_session, PersonMapper())


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


@pytest.fixture(scope="session")
def identity_provider_with_incorrect_permissions() -> Mock:
    identity_provider = Mock()
    identity_provider.get_permissions = Mock(return_value=0)

    return identity_provider
