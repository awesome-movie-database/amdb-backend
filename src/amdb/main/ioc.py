from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.orm import Session, sessionmaker

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_user import CreateUser
from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.domain.services.review_movie import ReviewMovie
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.application.command_handlers.review_movie import ReviewMovieHandler
from amdb.application.query_handlers.login import LoginHandler
from amdb.application.query_handlers.get_movies import GetMoviesHandler
from amdb.application.query_handlers.get_movie import GetMovieHandler
from amdb.application.query_handlers.get_movie_ratings import GetMovieRatingsHandler
from amdb.application.query_handlers.get_rating import GetRatingHandler
from amdb.application.query_handlers.get_movie_reviews import GetMovieReviewsHandler
from amdb.application.query_handlers.get_review import GetReviewHandler
from amdb.infrastructure.persistence.sqlalchemy.gateway_factory import (
    build_sqlalchemy_gateway_factory,
)
from amdb.infrastructure.persistence.redis.gateways.permissions import RedisPermissionsGateway
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.password_manager.password_manager import HashingPasswordManager
from amdb.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):
    def __init__(
        self,
        sessionmaker: sessionmaker[Session],
        permissions_gateway: RedisPermissionsGateway,
        hasher: Hasher,
    ) -> None:
        self._sessionmaker = sessionmaker
        self._permissions_gateway = permissions_gateway
        self._hasher = hasher

    @contextmanager
    def register_user(self) -> Iterator[RegisterUserHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            hashing_password_manager = HashingPasswordManager(
                hasher=self._hasher,
                user_password_hash_gateway=gateway_factory.user_password_hash(),
            )
            yield RegisterUserHandler(
                create_user=CreateUser(),
                user_gateway=gateway_factory.user(),
                permissions_gateway=self._permissions_gateway,
                unit_of_work=gateway_factory.unit_of_work(),
                password_manager=hashing_password_manager,
            )

    @contextmanager
    def login(self) -> Iterator[LoginHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            hashing_password_manager = HashingPasswordManager(
                hasher=self._hasher,
                user_password_hash_gateway=gateway_factory.user_password_hash(),
            )
            yield LoginHandler(
                access_concern=AccessConcern(),
                user_gateway=gateway_factory.user(),
                permissions_gateway=self._permissions_gateway,
                password_manager=hashing_password_manager,
            )

    @contextmanager
    def get_movies(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetMoviesHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetMoviesHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetMovieHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def create_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[CreateMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield CreateMovieHandler(
                access_concern=AccessConcern(),
                create_movie=CreateMovie(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                unit_of_work=gateway_factory.unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def delete_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[DeleteMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield DeleteMovieHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                rating_gateway=gateway_factory.rating(),
                review_gateway=gateway_factory.review(),
                unit_of_work=gateway_factory.unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_movie_ratings(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetMovieRatingsHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetMovieRatingsHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                rating_gateway=gateway_factory.rating(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_rating(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetRatingHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetRatingHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                rating_gateway=gateway_factory.rating(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def rate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[RateMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield RateMovieHandler(
                access_concern=AccessConcern(),
                rate_movie=RateMovie(),
                permissions_gateway=self._permissions_gateway,
                user_gateway=gateway_factory.user(),
                movie_gateway=gateway_factory.movie(),
                rating_gateway=gateway_factory.rating(),
                unit_of_work=gateway_factory.unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def unrate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[UnrateMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield UnrateMovieHandler(
                access_concern=AccessConcern(),
                unrate_movie=UnrateMovie(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                rating_gateway=gateway_factory.rating(),
                unit_of_work=gateway_factory.unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_movie_reviews(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetMovieReviewsHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetMovieReviewsHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.movie(),
                review_gateway=gateway_factory.review(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_review(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetReviewHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield GetReviewHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                review_gateway=gateway_factory.review(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def review_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[ReviewMovieHandler]:
        with build_sqlalchemy_gateway_factory(self._sessionmaker) as gateway_factory:
            yield ReviewMovieHandler(
                access_concern=AccessConcern(),
                review_movie=ReviewMovie(),
                permissions_gateway=self._permissions_gateway,
                user_gateway=gateway_factory.user(),
                movie_gateway=gateway_factory.movie(),
                review_gateway=gateway_factory.review(),
                unit_of_work=gateway_factory.unit_of_work(),
                identity_provider=identity_provider,
            )
