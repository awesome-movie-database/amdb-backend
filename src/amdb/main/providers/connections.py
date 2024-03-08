from typing import Iterable, cast

from dishka import Provider, Scope, provide
from sqlalchemy import Connection, Engine, create_engine
from redis import Redis

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig


class ConnectionsProvider(Provider):
    @provide(scope=Scope.APP)
    def sqlaclhemy_engine(
        self,
        postgres_config: PostgresConfig,
    ) -> Engine:
        return create_engine(postgres_config.url)

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_connection(
        self,
        sqlalchemy_engine: Engine,
    ) -> Iterable[Connection]:
        with sqlalchemy_engine.connect() as conn:
            yield conn

    @provide(scope=Scope.APP)
    def redis(self, redis_config: RedisConfig) -> Redis:
        redis = Redis.from_url(
            url=redis_config.url,
            decode_responses=True,
        )
        return cast(Redis, redis)
