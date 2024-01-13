import pytest
from sqlalchemy.orm import Session

from amdb.infrastructure.persistence.sqlalchemy.gateways.user import SQLAlchemyUserGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.movie import SQLAlchemyMovieGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.rating import SQLAlchemyRatingGateway
from amdb.infrastructure.persistence.sqlalchemy.gateways.user_password import (
    SQLAlchemyUserPasswordHashGateway,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.user import UserMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.movie import MovieMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.rating import RatingMapper
from amdb.infrastructure.persistence.sqlalchemy.mappers.user_password import UserPasswordHashMapper
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.security.password_manager import HashingPasswordManager
from amdb.infrastructure.permissions_gateway import InMemoryPermissionsGateway


@pytest.fixture(scope="package")
def permissions_gateway() -> InMemoryPermissionsGateway:
    return InMemoryPermissionsGateway()


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
