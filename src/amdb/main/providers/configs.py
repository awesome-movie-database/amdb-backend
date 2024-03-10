from dishka import Provider, Scope, provide

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig


class ConfigsProvider(Provider):
    def __init__(
        self,
        *,
        postgres_config: PostgresConfig,
        redis_config: RedisConfig,
    ) -> None:
        super().__init__()
        self._postgres_config = postgres_config
        self._redis_config = redis_config

    @provide(scope=Scope.APP)
    def postgres_config(self) -> PostgresConfig:
        return self._postgres_config

    @provide(scope=Scope.APP)
    def redis_config(self) -> RedisConfig:
        return self._redis_config
