from sqlalchemy.orm import Session

from .gateways.user import SQLAlchemyUserGateway
from .gateways.movie import SQLAlchemyMovieGateway
from .gateways.rating import SQLAlchemyRatingGateway
from .gateways.user_password import SQLAlchemyUserPasswordHashGateway
from .mappers.user import UserMapper
from .mappers.movie import MovieMapper
from .mappers.rating import RatingMapper
from .mappers.user_password import UserPasswordHashMapper


class GatewayFactory:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_user_gateway(self) -> SQLAlchemyUserGateway:
        return SQLAlchemyUserGateway(self._session, UserMapper())

    def create_movie_gateway(self) -> SQLAlchemyMovieGateway:
        return SQLAlchemyMovieGateway(self._session, MovieMapper())

    def create_rating_gateway(self) -> SQLAlchemyRatingGateway:
        return SQLAlchemyRatingGateway(self._session, RatingMapper())

    def create_user_password_hash_gateway(self) -> SQLAlchemyUserPasswordHashGateway:
        return SQLAlchemyUserPasswordHashGateway(self._session, UserPasswordHashMapper())

    def create_unit_of_work(self) -> Session:
        return self._session
