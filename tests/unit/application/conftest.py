from typing import Iterator
from unittest.mock import Mock

import pytest
from sqlalchemy import Connection, Engine, create_engine
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.models.base import Model
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
from amdb.infrastructure.persistence.sqlalchemy.mappers.password_hash import (
    PasswordHashMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.non_detailed_movie import (
    NonDetailedMovieViewModelsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.detailed_movie import (
    DetailedMovieViewModelMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.detailed_review import (
    DetailedReviewViewModelsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.view_models.my_detailed_ratings import (
    MyDetailedRatingsViewModelMapper,
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
