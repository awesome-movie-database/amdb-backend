from typing import cast

from fastapi import FastAPI
from sqlalchemy import create_engine
from redis.client import Redis

from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.infrastructure.persistence.redis.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.password_manager.hash_computer import HashComputer
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.main.ioc import IoC


def setup_dependecies(
    app: FastAPI,
    session_config: SessionConfig,
    postgres_config: PostgresConfig,
    redis_config: RedisConfig,
) -> None:
    redis = Redis.from_url(redis_config.url, decode_responses=True)
    session_mapper = SessionMapper(
        redis=cast(Redis, redis),
        session_lifetime=session_config.lifetime,
    )
    app.dependency_overrides[Stub(SessionMapper)] = lambda: session_mapper  # type: ignore

    permissions_mapper = PermissionsMapper(cast(Redis, redis))
    app.dependency_overrides[Stub(PermissionsMapper)] = (
        lambda: permissions_mapper
    )  # type: ignore

    sqlalchemy_engine = create_engine(postgres_config.url)
    ioc = IoC(
        sqlalchemy_engine=sqlalchemy_engine,
        permissions_mapper=permissions_mapper,
        hash_computer=HashComputer(),
    )
    app.dependency_overrides[HandlerFactory] = lambda: ioc  # type: ignore

    session_processor = SessionProcessor()
    app.dependency_overrides[Stub(SessionProcessor)] = (
        lambda: session_processor
    )  # type: ignore
