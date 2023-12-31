from sqlalchemy.orm import Session

from .gateways.user import SQLAlchemyUserGateway
from .gateways.movie import SQLAlchemyMovieGateway
from .gateways.rating import SQLAlchemyRatingGateway
from .mappers.user import UserMapper
from .mappers.movie import MovieMapper
from .mappers.rating import RatingMapper


class GatewayFactory:
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def create_user_gateway(self) -> SQLAlchemyUserGateway:
        return SQLAlchemyUserGateway(self._session, UserMapper())
    
    def create_movie_gateway(self) -> SQLAlchemyMovieGateway:
        return SQLAlchemyMovieGateway(self._session, MovieMapper())
    
    def create_rating_gateway(self) -> SQLAlchemyRatingGateway:
        return SQLAlchemyRatingGateway(self._session, RatingMapper())
