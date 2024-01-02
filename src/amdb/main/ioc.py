from contextlib import contextmanager
from typing import Iterator

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_user import CreateUser
from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.command_handlers.create_user import CreateUserHandler
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.infrastructure.database.builders import BuildGatewayFactory
from amdb.infrastructure.in_memory.permissions_gateway import InMemoryPermissionsGateway
from amdb.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):
    def __init__(
        self,
        build_gateway_factory: BuildGatewayFactory,
        permissions_gateway: InMemoryPermissionsGateway,
    ) -> None:
        self._build_gateway_factory = build_gateway_factory
        self._permissions_gateway = permissions_gateway

    @contextmanager
    def create_user(self) -> Iterator[CreateUserHandler]:
        with self._build_gateway_factory() as gateway_factory:
            yield CreateUserHandler(
                create_user=CreateUser(),
                user_gateway=gateway_factory.create_user_gateway(),
                unit_of_work=gateway_factory.create_unit_of_work(),
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
