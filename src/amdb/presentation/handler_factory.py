from abc import ABC, abstractmethod
from typing import ContextManager

from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.command_handlers.create_movie import CreateMovieHandler
from amdb.application.command_handlers.delete_movie import DeleteMovieHandler
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.application.command_handlers.review_movie import ReviewMovieHandler
from amdb.application.query_handlers.login import LoginHandler
from amdb.application.query_handlers.detailed_movie import (
    GetDetailedMovieHandler,
)
from amdb.application.query_handlers.non_detailed_movies import (
    GetNonDetailedMoviesHandler,
)
from amdb.application.query_handlers.reviews import GetReviewsHandler


class HandlerFactory(ABC):
    @abstractmethod
    def register_user(self) -> ContextManager[RegisterUserHandler]:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> ContextManager[LoginHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_non_detailed_movies(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetNonDetailedMoviesHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_detailed_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetDetailedMovieHandler]:
        raise NotImplementedError

    @abstractmethod
    def create_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[CreateMovieHandler]:
        raise NotImplementedError

    @abstractmethod
    def delete_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[DeleteMovieHandler]:
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

    @abstractmethod
    def get_reviews(self) -> ContextManager[GetReviewsHandler]:
        raise NotImplementedError

    @abstractmethod
    def review_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[ReviewMovieHandler]:
        raise NotImplementedError
