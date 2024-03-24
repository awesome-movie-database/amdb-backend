import os
from typing import cast

import pytest
from redis.client import Redis

from amdb.infrastructure.persistence.sqlalchemy.config import (
    load_postgres_config_from_toml,
)
from amdb.infrastructure.persistence.redis.config import (
    load_redis_config_from_toml,
)


CONFIG_PATH = os.getenv("TEST_CONFIG_PATH")


@pytest.fixture(scope="session")
def postgres_url() -> str:
    postgres_config = load_postgres_config_from_toml(CONFIG_PATH)
    return postgres_config.url


@pytest.fixture(scope="session")
def redis() -> Redis:
    redis_config = load_redis_config_from_toml(CONFIG_PATH)
    redis = Redis.from_url(redis_config.url, decode_responses=True)
    return cast(Redis, redis)
