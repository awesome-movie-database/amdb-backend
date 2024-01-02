from abc import ABC, abstractmethod
from typing import ContextManager

from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.command_handlers.create_user import CreateUserHandler
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler


class HandlerFactory(ABC):
    @abstractmethod
    def create_user(self) -> ContextManager[CreateUserHandler]:
        raise NotImplementedError

    @abstractmethod
    def create_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[CreateMovieHandler]:
        raise NotImplementedError

    @abstractmethod
    def rate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[RateMovieHandler]:
        raise NotImplementedError

    @abstractmethod
    def unrate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[UnrateMovieHandler]:
        raise NotImplementedError
