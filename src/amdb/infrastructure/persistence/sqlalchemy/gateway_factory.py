from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.orm import Session, sessionmaker

from .gateways.user import SQLAlchemyUserGateway
from .gateways.person import SQLAlchemyPersonGateway
from .gateways.movie import SQLAlchemyMovieGateway
from .gateways.rating import SQLAlchemyRatingGateway
from .gateways.user_password_hash import SQLAlchemyUserPasswordHashGateway
from .mappers.user import UserMapper
from .mappers.person import PersonMapper
from .mappers.movie import MovieMapper
from .mappers.rating import RatingMapper
from .mappers.user_password_hash import UserPasswordHashMapper


@contextmanager
def build_sqlalchemy_gateway_factory(
    sessionmaker: sessionmaker[Session],
) -> Iterator["SQLAlchemyGatewayFactory"]:
    session = sessionmaker()
    yield SQLAlchemyGatewayFactory(session)
    session.close()


class SQLAlchemyGatewayFactory:
    def __init__(self, session: Session) -> None:
        self._session = session

    def user(self) -> SQLAlchemyUserGateway:
        return SQLAlchemyUserGateway(self._session, UserMapper())

    def person(self) -> SQLAlchemyPersonGateway:
        return SQLAlchemyPersonGateway(self._session, PersonMapper())

    def movie(self) -> SQLAlchemyMovieGateway:
        return SQLAlchemyMovieGateway(self._session, MovieMapper())

    def rating(self) -> SQLAlchemyRatingGateway:
        return SQLAlchemyRatingGateway(self._session, RatingMapper())

    def user_password_hash(self) -> SQLAlchemyUserPasswordHashGateway:
        return SQLAlchemyUserPasswordHashGateway(self._session, UserPasswordHashMapper())

    def unit_of_work(self) -> Session:
        return self._session
