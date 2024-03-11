from dishka import Provider, Scope, alias, provide
from sqlalchemy import Connection
from redis import Redis

from amdb.application.common.gateways import (
    UserGateway,
    MovieGateway,
    RatingGateway,
    ReviewGateway,
    MovieForLaterGateway,
    PermissionsGateway,
)
from amdb.application.common.readers import (
    DetailedMovieViewModelReader,
    DetailedReviewViewModelsReader,
    RatingForExportViewModelsReader,
    MyDetailedRatingsViewModelReader,
    NonDetailedMovieViewModelsReader,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.infrastructure.password_manager.password_hash_gateway import (
    PasswordHashGateway,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers import (
    UserMapper,
    MovieMapper,
    RatingMapper,
    ReviewMapper,
    MovieForLaterMapper,
    PermissionsMapper,
    PasswordHashMapper,
    DetailedMovieViewModelMapper,
    DetailedReviewViewModelsMapper,
    RatingForExportViewModelMapper,
    MyDetailedRatingsViewModelMapper,
    NonDetailedMovieViewModelsMapper,
)
from amdb.infrastructure.persistence.redis.cache.permissions_mapper import (
    PermissionsMapperCacheProvider,
)
from amdb.infrastructure.persistence.caching.permissions_mapper import (
    CachingPermissionsMapper,
)


class EntityMappersProvider(Provider):
    scope = Scope.REQUEST

    user = provide(UserMapper, provides=UserGateway)
    movie = provide(MovieMapper, provides=MovieGateway)
    rating = provide(RatingMapper, provides=RatingGateway)
    review = provide(ReviewMapper, provides=ReviewGateway)
    movie_for_later = provide(
        MovieForLaterMapper,
        provides=MovieForLaterGateway,
    )

    unit_of_work = alias(source=Connection, provides=UnitOfWork)


class ApplicationModelMappersProvider(Provider):
    scope = Scope.REQUEST

    password_hash = provide(
        PasswordHashMapper,
        provides=PasswordHashGateway,
    )

    @provide
    def permissions(
        self,
        redis: Redis,
        sqlalchemy_connection: Connection,
    ) -> PermissionsGateway:
        return CachingPermissionsMapper(
            permissions_mapper=PermissionsMapper(sqlalchemy_connection),
            cache_provider=PermissionsMapperCacheProvider(redis),
        )


class ViewModelMappersProvider(Provider):
    scope = Scope.REQUEST

    detailed_movie = provide(
        DetailedMovieViewModelMapper,
        provides=DetailedMovieViewModelReader,
    )
    detailed_review = provide(
        DetailedReviewViewModelsMapper,
        provides=DetailedReviewViewModelsReader,
    )
    rating_for_export = provide(
        RatingForExportViewModelMapper,
        provides=RatingForExportViewModelsReader,
    )
    my_detailed_ratings = provide(
        MyDetailedRatingsViewModelMapper,
        provides=MyDetailedRatingsViewModelReader,
    )
    non_detailed_movie = provide(
        NonDetailedMovieViewModelsMapper,
        provides=NonDetailedMovieViewModelsReader,
    )
