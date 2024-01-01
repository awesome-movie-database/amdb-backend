import pytest
from sqlalchemy.orm import Session

from amdb.infrastructure.database.gateways.user import SQLAlchemyUserGateway
from amdb.infrastructure.database.gateways.movie import SQLAlchemyMovieGateway
from amdb.infrastructure.database.gateways.rating import SQLAlchemyRatingGateway
from amdb.infrastructure.database.mappers.user import UserMapper
from amdb.infrastructure.database.mappers.movie import MovieMapper
from amdb.infrastructure.database.mappers.rating import RatingMapper
from amdb.infrastructure.in_memory.permissions_gateway import InMemoryPermissionsGateway


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
def unit_of_work(sqlalchemy_session: Session) -> Session:
    return sqlalchemy_session
