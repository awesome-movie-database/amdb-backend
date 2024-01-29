from abc import ABC, abstractmethod
from typing import ContextManager

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
from amdb.application.query_handlers.get_my_ratings import GetMyRatingsHandler
from amdb.application.query_handlers.get_rating import GetRatingHandler
from amdb.application.query_handlers.get_movie_reviews import GetMovieReviewsHandler
from amdb.application.query_handlers.get_review import GetReviewHandler


class HandlerFactory(ABC):
    @abstractmethod
    def register_user(self) -> ContextManager[RegisterUserHandler]:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> ContextManager[LoginHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_movies(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetMoviesHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetMovieHandler]:
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
    def get_movie_ratings(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetMovieRatingsHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_my_ratings(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetMyRatingsHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_rating(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetRatingHandler]:
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
    def get_movie_reviews(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetMovieReviewsHandler]:
        raise NotImplementedError

    @abstractmethod
    def get_review(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[GetReviewHandler]:
        raise NotImplementedError

    @abstractmethod
    def review_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> ContextManager[ReviewMovieHandler]:
        raise NotImplementedError
