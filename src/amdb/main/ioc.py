from contextlib import contextmanager
from typing import Iterator

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_user import CreateUser
from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.infrastructure.persistence.sqlalchemy.builders import BuildGatewayFactory
from amdb.infrastructure.permissions_gateway import InMemoryPermissionsGateway
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.security.password_manager import HashingPasswordManager
from amdb.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):
    def __init__(
        self,
        build_gateway_factory: BuildGatewayFactory,
        permissions_gateway: InMemoryPermissionsGateway,
        hasher: Hasher,
    ) -> None:
        self._build_gateway_factory = build_gateway_factory
        self._permissions_gateway = permissions_gateway
        self._hasher = hasher

    @contextmanager
    def register_user(self) -> Iterator[RegisterUserHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield RegisterUserHandler(
                create_user=CreateUser(),
                user_gateway=gateway_factory.create_user_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
                password_manager=HashingPasswordManager(
                    hasher=self._hasher,
                    user_password_hash_gateway=gateway_factory.create_user_password_hash_gateway(),
                ),
            )

    @contextmanager
    def create_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[CreateMovieHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield CreateMovieHandler(
                access_concern=AccessConcern(),
                create_movie=CreateMovie(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.create_movie_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def delete_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[DeleteMovieHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield DeleteMovieHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_gateway,
                movie_gateway=gateway_factory.create_movie_gateway(),
                rating_gateway=gateway_factory.create_rating_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def rate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[RateMovieHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield RateMovieHandler(
                access_concern=AccessConcern(),
                rate_movie=RateMovie(),
                permissions_gateway=self._permissions_gateway,
                user_gateway=gateway_factory.create_user_gateway(),
                movie_gateway=gateway_factory.create_movie_gateway(),
                rating_gateway=gateway_factory.create_rating_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
                identity_provider=identity_provider,
            )

    @contextmanager
    def unrate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[UnrateMovieHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield UnrateMovieHandler(
                access_concern=AccessConcern(),
                unrate_movie=UnrateMovie(),
                permissions_gateway=self._permissions_gateway,
                user_gateway=gateway_factory.create_user_gateway(),
                movie_gateway=gateway_factory.create_movie_gateway(),
                rating_gateway=gateway_factory.create_rating_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
                identity_provider=identity_provider,
            )
