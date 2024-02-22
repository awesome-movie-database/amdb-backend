from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_user import CreateUser
from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.domain.services.review_movie import ReviewMovie
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
from amdb.infrastructure.persistence.sqlalchemy.mappers.entities.user import (
    UserMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.entities.movie import (
    MovieMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.entities.rating import (
    RatingMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.entities.review import (
    ReviewMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.non_detailed_movie import (
    NonDetailedMovieViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.detailed_movie import (
    DetailedMovieViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.review import (
    ReviewViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.password_hash import (
    PasswordHashMapper,
)
from amdb.infrastructure.persistence.redis.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.password_manager.hash_computer import HashComputer
from amdb.infrastructure.password_manager.password_manager import (
    HashingPasswordManager,
)
from amdb.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):
    def __init__(
        self,
        sqlalchemy_engine: Engine,
        permissions_mapper: PermissionsMapper,
        hash_computer: HashComputer,
    ) -> None:
        self._sqlalchemy_engine = sqlalchemy_engine
        self._permissions_mapper = permissions_mapper
        self._hash_computer = hash_computer

    @contextmanager
    def register_user(self) -> Iterator[RegisterUserHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            password_manager = HashingPasswordManager(
                hash_computer=self._hash_computer,
                password_hash_gateway=PasswordHashMapper(
                    sqlalchemy_connection,
                ),
            )
            yield RegisterUserHandler(
                create_user=CreateUser(),
                user_gateway=UserMapper(sqlalchemy_connection),
                permissions_gateway=self._permissions_mapper,
                unit_of_work=sqlalchemy_connection,
                password_manager=password_manager,
            )

    @contextmanager
    def login(self) -> Iterator[LoginHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            password_manager = HashingPasswordManager(
                hash_computer=self._hash_computer,
                password_hash_gateway=PasswordHashMapper(
                    sqlalchemy_connection,
                ),
            )
            yield LoginHandler(
                access_concern=AccessConcern(),
                user_gateway=UserMapper(sqlalchemy_connection),
                permissions_gateway=self._permissions_mapper,
                password_manager=password_manager,
            )

    @contextmanager
    def get_non_detailed_movies(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetNonDetailedMoviesHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield GetNonDetailedMoviesHandler(
                non_detailed_movie_reader=NonDetailedMovieViewModelMapper(
                    sqlalchemy_connection,
                ),
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_detailed_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[GetDetailedMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield GetDetailedMovieHandler(
                detailed_movie_reader=DetailedMovieViewModelMapper(
                    sqlalchemy_connection,
                ),
                identity_provider=identity_provider,
            )

    @contextmanager
    def create_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[CreateMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield CreateMovieHandler(
                access_concern=AccessConcern(),
                create_movie=CreateMovie(),
                permissions_gateway=self._permissions_mapper,
                movie_gateway=MovieMapper(sqlalchemy_connection),
                unit_of_work=sqlalchemy_connection,
                identity_provider=identity_provider,
            )

    @contextmanager
    def delete_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[DeleteMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield DeleteMovieHandler(
                access_concern=AccessConcern(),
                permissions_gateway=self._permissions_mapper,
                movie_gateway=MovieMapper(sqlalchemy_connection),
                rating_gateway=RatingMapper(sqlalchemy_connection),
                review_gateway=ReviewMapper(sqlalchemy_connection),
                unit_of_work=sqlalchemy_connection,
                identity_provider=identity_provider,
            )

    @contextmanager
    def rate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[RateMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield RateMovieHandler(
                access_concern=AccessConcern(),
                rate_movie=RateMovie(),
                permissions_gateway=self._permissions_mapper,
                user_gateway=UserMapper(sqlalchemy_connection),
                movie_gateway=MovieMapper(sqlalchemy_connection),
                rating_gateway=RatingMapper(sqlalchemy_connection),
                unit_of_work=sqlalchemy_connection,
                identity_provider=identity_provider,
            )

    @contextmanager
    def unrate_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[UnrateMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield UnrateMovieHandler(
                access_concern=AccessConcern(),
                unrate_movie=UnrateMovie(),
                permissions_gateway=self._permissions_mapper,
                movie_gateway=MovieMapper(sqlalchemy_connection),
                rating_gateway=RatingMapper(sqlalchemy_connection),
                unit_of_work=sqlalchemy_connection,
                identity_provider=identity_provider,
            )

    @contextmanager
    def get_reviews(self) -> Iterator[GetReviewsHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield GetReviewsHandler(
                movie_gateway=MovieMapper(sqlalchemy_connection),
                review_view_model_reader=ReviewViewModelMapper(
                    sqlalchemy_connection,
                ),
            )

    @contextmanager
    def review_movie(
        self,
        identity_provider: IdentityProvider,
    ) -> Iterator[ReviewMovieHandler]:
        with self._sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield ReviewMovieHandler(
                access_concern=AccessConcern(),
                review_movie=ReviewMovie(),
                permissions_gateway=self._permissions_mapper,
                user_gateway=UserMapper(sqlalchemy_connection),
                movie_gateway=MovieMapper(sqlalchemy_connection),
                review_gateway=ReviewMapper(sqlalchemy_connection),
                unit_of_work=sqlalchemy_connection,
                identity_provider=identity_provider,
            )
