from typing import Iterator
from unittest.mock import Mock

import pytest
from sqlalchemy import Connection, Engine, create_engine
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.models.base import Model
from amdb.infrastructure.persistence.sqlalchemy.mappers import (
    UserMapper,
    MovieMapper,
    RatingMapper,
    ReviewMapper,
    MovieForLaterMapper,
    DetailedMovieViewModelMapper,
    DetailedReviewViewModelsMapper,
    RatingForExportViewModelMapper,
    MyDetailedRatingsViewModelMapper,
    NonDetailedMovieViewModelsMapper,
    MyDetailedWatchlistViewModelMapper,
    PasswordHashMapper,
    PermissionsMapper,
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


@pytest.fixture(scope="session")
def sqlalchemy_engine(postgres_url: str) -> Engine:
    return create_engine(url=postgres_url)


@pytest.fixture(autouse=True)
def clear_database(sqlalchemy_engine: Engine) -> Iterator[None]:
    Model.metadata.create_all(sqlalchemy_engine)
    yield
    Model.metadata.drop_all(sqlalchemy_engine)


@pytest.fixture
def sqlalchemy_connection(sqlalchemy_engine: Engine) -> Iterator[Connection]:
    connection = sqlalchemy_engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def permissions_gateway(
    redis: Redis,
    sqlalchemy_connection: Connection,
) -> CachingPermissionsMapper:
    return CachingPermissionsMapper(
        permissions_mapper=PermissionsMapper(sqlalchemy_connection),
        cache_provider=PermissionsMapperCacheProvider(redis),
    )


@pytest.fixture
def user_gateway(sqlalchemy_connection: Connection) -> UserMapper:
    return UserMapper(sqlalchemy_connection)


@pytest.fixture
def movie_gateway(sqlalchemy_connection: Connection) -> MovieMapper:
    return MovieMapper(sqlalchemy_connection)


@pytest.fixture
def rating_gateway(sqlalchemy_connection: Connection) -> RatingMapper:
    return RatingMapper(sqlalchemy_connection)


@pytest.fixture
def review_gateway(sqlalchemy_connection: Connection) -> ReviewMapper:
    return ReviewMapper(sqlalchemy_connection)


@pytest.fixture
def movie_for_later_gateway(
    sqlalchemy_connection: Connection,
) -> MovieForLaterMapper:
    return MovieForLaterMapper(sqlalchemy_connection)


@pytest.fixture
def detailed_movie_reader(
    sqlalchemy_connection: Connection,
) -> DetailedMovieViewModelMapper:
    return DetailedMovieViewModelMapper(sqlalchemy_connection)


@pytest.fixture
def non_detailed_movies_reader(
    sqlalchemy_connection: Connection,
) -> NonDetailedMovieViewModelsMapper:
    return NonDetailedMovieViewModelsMapper(sqlalchemy_connection)


@pytest.fixture
def detailed_reviews_reader(
    sqlalchemy_connection: Connection,
) -> DetailedMovieViewModelMapper:
    return DetailedReviewViewModelsMapper(sqlalchemy_connection)


@pytest.fixture
def my_detailed_ratings_reader(
    sqlalchemy_connection: Connection,
) -> MyDetailedRatingsViewModelMapper:
    return MyDetailedRatingsViewModelMapper(sqlalchemy_connection)


@pytest.fixture
def ratings_for_export_reader(
    sqlalchemy_connection: Connection,
) -> RatingForExportViewModelMapper:
    return RatingForExportViewModelMapper(sqlalchemy_connection)


@pytest.fixture
def my_detailed_watchlist_reader(
    sqlalchemy_connection: Connection,
) -> MyDetailedWatchlistViewModelMapper:
    return MyDetailedWatchlistViewModelMapper(sqlalchemy_connection)


@pytest.fixture
def password_manager(
    sqlalchemy_connection: Connection,
) -> HashingPasswordManager:
    return HashingPasswordManager(
        hash_computer=HashComputer(),
        password_hash_gateway=PasswordHashMapper(sqlalchemy_connection),
    )


@pytest.fixture
def unit_of_work(sqlalchemy_connection: Connection) -> Connection:
    return sqlalchemy_connection


@pytest.fixture(scope="session")
def identity_provider_with_incorrect_permissions() -> Mock:
    identity_provider = Mock()
    identity_provider.permissions = Mock(return_value=0)

    return identity_provider
