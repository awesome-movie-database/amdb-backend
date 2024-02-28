from typing import Iterable, cast

from dishka import Provider, Scope, provide, alias
from sqlalchemy import Connection, Engine, create_engine
from redis import Redis

from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.create_user import CreateUser
from amdb.domain.services.update_profile import UpdateProfile
from amdb.domain.services.create_movie import CreateMovie
from amdb.domain.services.rate_movie import RateMovie
from amdb.domain.services.unrate_movie import UnrateMovie
from amdb.domain.services.review_movie import ReviewMovie
from amdb.domain.validators.email import ValidateEmail
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.rating import RatingGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.readers.detailed_movie import (
    DetailedMovieViewModelReader,
)
from amdb.application.common.readers.non_detailed_movie import (
    NonDetailedMovieViewModelsReader,
)
from amdb.application.common.readers.detailed_review import (
    DetailedReviewViewModelsReader,
)
from amdb.application.common.readers.my_detailed_ratings import (
    MyDetailedRatingsViewModelReader,
)
from amdb.application.common.password_manager import PasswordManager
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.command_handlers.update_my_profile import (
    UpdateMyProfileHandler,
)
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
from amdb.application.query_handlers.detailed_reviews import (
    GetDetailedReviewsHandler,
)
from amdb.application.query_handlers.my_detailed_ratings import (
    GetMyDetailedRatingsHandler,
)
from amdb.application.query_handlers.export_my_ratings import (
    ExportMyRatingsHandler,
)
from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
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
from amdb.infrastructure.persistence.sqlalchemy.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.password_hash import (
    PasswordHashMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.detailed_movie import (
    DetailedMovieViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.non_detailed_movie import (
    NonDetailedMovieViewModelsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.detailed_review import (
    DetailedReviewViewModelsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.my_detailed_ratings import (
    MyDetailedRatingsViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.rating_for_export import (
    RatingForExportViewModelMapper,
)
from amdb.infrastructure.persistence.redis.cache.permissions_mapper import (
    PermissionsMapperCacheProvider,
)
from amdb.infrastructure.persistence.caching.permissions_mapper import (
    CachingPermissionsMapper,
)
from amdb.infrastructure.password_manager.hash_computer import HashComputer
from amdb.infrastructure.password_manager.password_manager import (
    HashingPasswordManager,
)
from amdb.infrastructure.converters.ratings_for_export import (
    RealRatingsForExportConverter,
)
from amdb.presentation.create_handler import CreateHandler


class ConnectionsProvider(Provider):
    scope = Scope.APP

    def __init__(
        self,
        *,
        postgres_config: PostgresConfig,
        redis_config: RedisConfig,
    ) -> None:
        super().__init__()
        self._postgsres_config = postgres_config
        self._redis_config = redis_config

    @provide
    def sqlaclhemy_engine(self) -> Engine:
        return create_engine(self._postgsres_config.url)

    @provide
    def redis(self) -> Redis:
        redis = Redis.from_url(
            url=self._redis_config.url,
            decode_responses=True,
        )
        return cast(Redis, redis)

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_connection(
        self,
        sqlalchemy_engine: Engine,
    ) -> Iterable[Connection]:
        with sqlalchemy_engine.connect() as sqlalchemy_connection:
            yield sqlalchemy_connection


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = provide(source=UserMapper, provides=UserGateway)
    movie_gateway = provide(source=MovieMapper, provides=MovieGateway)
    rating_gateway = provide(source=RatingMapper, provides=RatingGateway)
    review_gateway = provide(source=ReviewMapper, provides=ReviewGateway)
    detailed_movie_reader = provide(
        source=DetailedMovieViewModelMapper,
        provides=DetailedMovieViewModelReader,
    )
    non_detailed_movie_reader = provide(
        source=NonDetailedMovieViewModelsMapper,
        provides=NonDetailedMovieViewModelsReader,
    )
    detailed_review_reader = provide(
        source=DetailedReviewViewModelsMapper,
        provides=DetailedReviewViewModelsReader,
    )
    my_detailed_ratings_reader = provide(
        source=MyDetailedRatingsViewModelMapper,
        provides=MyDetailedRatingsViewModelReader,
    )

    unit_of_work = alias(source=Connection, provides=UnitOfWork)

    @provide
    def permissions_mapper(
        self,
        sqlalchemy_connection: Connection,
        redis: Redis,
    ) -> PermissionsMapper:
        permissions_mapper = PermissionsMapper(sqlalchemy_connection)
        cache_provider = PermissionsMapperCacheProvider(redis)
        return CachingPermissionsMapper(  # type: ignore
            permissions_mapper=permissions_mapper,
            cache_provider=cache_provider,
        )

    @provide
    def permissions_gateway(
        self,
        sqlalchemy_connection: Connection,
        redis: Redis,
    ) -> PermissionsGateway:
        permissions_mapper = PermissionsMapper(sqlalchemy_connection)
        cache_provider = PermissionsMapperCacheProvider(redis)
        return CachingPermissionsMapper(
            permissions_mapper=permissions_mapper,
            cache_provider=cache_provider,
        )

    @provide
    def password_manager(
        self,
        sqlalchemy_connection: Connection,
    ) -> PasswordManager:
        password_hash_mapper = PasswordHashMapper(sqlalchemy_connection)
        return HashingPasswordManager(
            hash_computer=HashComputer(),
            password_hash_gateway=password_hash_mapper,
        )


class HandlersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register_user_handler(
        self,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        unit_of_work: UnitOfWork,
        password_manager: PasswordManager,
    ) -> RegisterUserHandler:
        return RegisterUserHandler(
            create_user=CreateUser(validate_email=ValidateEmail()),
            user_gateway=user_gateway,
            permissions_gateway=permissions_gateway,
            unit_of_work=unit_of_work,
            password_manager=password_manager,
        )

    @provide
    def login_handler(
        self,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        password_manager: PasswordManager,
    ) -> LoginHandler:
        return LoginHandler(
            access_concern=AccessConcern(),
            user_gateway=user_gateway,
            permissions_gateway=permissions_gateway,
            password_manager=password_manager,
        )

    @provide
    def create_movie_handler(
        self,
        movie_gateway: MovieGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateMovieHandler:
        return CreateMovieHandler(
            create_movie=CreateMovie(),
            movie_gateway=movie_gateway,
            unit_of_work=unit_of_work,
        )

    @provide
    def delete_movie_handler(
        self,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
    ) -> DeleteMovieHandler:
        return DeleteMovieHandler(
            movie_gateway=movie_gateway,
            rating_gateway=rating_gateway,
            review_gateway=review_gateway,
            unit_of_work=unit_of_work,
        )

    @provide
    def get_detailed_reviews_handler(
        self,
        movie_gateway: MovieGateway,
        detailed_reviews_reader: DetailedReviewViewModelsReader,
    ) -> GetDetailedReviewsHandler:
        return GetDetailedReviewsHandler(
            movie_gateway=movie_gateway,
            detailed_reviews_reader=detailed_reviews_reader,
        )


class HandlerCreatorsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def update_my_profile_handler(
        self,
        user_gateway: UserGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[UpdateMyProfileHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> UpdateMyProfileHandler:
            return UpdateMyProfileHandler(
                update_profile=UpdateProfile(),
                user_gateway=user_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_detailed_movie_handler(
        self,
        detailed_movie_reader: DetailedMovieViewModelReader,
    ) -> CreateHandler[GetDetailedMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetDetailedMovieHandler:
            return GetDetailedMovieHandler(
                detailed_movie_reader=detailed_movie_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_non_detailed_movies_handler(
        self,
        non_detailed_movies_reader: NonDetailedMovieViewModelsReader,
    ) -> CreateHandler[GetNonDetailedMoviesHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetNonDetailedMoviesHandler:
            return GetNonDetailedMoviesHandler(
                non_detailed_movies_reader=non_detailed_movies_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_my_detailed_ratings_handler(
        self,
        my_detailed_ratings_reader: MyDetailedRatingsViewModelReader,
    ) -> CreateHandler[GetMyDetailedRatingsHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetMyDetailedRatingsHandler:
            return GetMyDetailedRatingsHandler(
                my_detailed_ratings_reader=my_detailed_ratings_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def rate_movie_handler(
        self,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[RateMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> RateMovieHandler:
            return RateMovieHandler(
                access_concern=AccessConcern(),
                rate_movie=RateMovie(),
                permissions_gateway=permissions_gateway,
                user_gateway=user_gateway,
                movie_gateway=movie_gateway,
                rating_gateway=rating_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def unrate_movie_handler(
        self,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[UnrateMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> UnrateMovieHandler:
            return UnrateMovieHandler(
                access_concern=AccessConcern(),
                unrate_movie=UnrateMovie(),
                permissions_gateway=permissions_gateway,
                movie_gateway=movie_gateway,
                rating_gateway=rating_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def review_movie_handler(
        self,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[ReviewMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> ReviewMovieHandler:
            return ReviewMovieHandler(
                access_concern=AccessConcern(),
                review_movie=ReviewMovie(),
                permissions_gateway=permissions_gateway,
                user_gateway=user_gateway,
                movie_gateway=movie_gateway,
                review_gateway=review_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def export_my_ratings_handler(
        self,
        sqlaclhemy_connection: Connection,
    ) -> CreateHandler[ExportMyRatingsHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> ExportMyRatingsHandler:
            return ExportMyRatingsHandler(
                ratings_for_export_reader=RatingForExportViewModelMapper(
                    connection=sqlaclhemy_connection,
                ),
                ratings_for_export_converter=RealRatingsForExportConverter(),
                identity_provider=identity_provider,
            )

        return create_handler
