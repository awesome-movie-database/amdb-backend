import os

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from .app import create_app


def main() -> None:
    path_to_config = os.getenv("CONFIG_PATH")
    if not path_to_config:
        message = "Path to config env var is not set"
        raise ValueError(message)

    postgres_config = PostgresConfig.from_toml(path_to_config)
    redis_config = RedisConfig.from_toml(path_to_config)

    app = create_app(
        postgres_config=postgres_config,
        redis_config=redis_config,
    )

    app()


main()
