from typing import cast
from uuid import UUID

import typer
from sqlalchemy import create_engine
from redis import Redis

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.persistence.redis.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.password_manager.hash_computer import HashComputer
from amdb.infrastructure.auth.raw.identity_provider import RawIdentityProvider
from amdb.presentation.cli.setup import setup_typer_command_handlers
from amdb.main.ioc import IoC


IDENTITY_PROVIDER_USER_ID = UserId(
    UUID("00000000-0000-0000-0000-000000000000"),
)
IDENTITY_PROVIDER_PERMISSIONS = 12


def create_app(
    postgres_config: PostgresConfig,
    redis_config: RedisConfig,
) -> typer.Typer:
    sqlalchemy_engine = create_engine(postgres_config.url)
    redis = Redis.from_url(redis_config.url, decode_responses=True)
    permissions_mapper = PermissionsMapper(cast(Redis, redis))

    ioc = IoC(
        sqlalchemy_engine=sqlalchemy_engine,
        permissions_mapper=permissions_mapper,
        hash_computer=HashComputer(),
    )
    raw_identity_provider = RawIdentityProvider(
        user_id=IDENTITY_PROVIDER_USER_ID,
        permissions=IDENTITY_PROVIDER_PERMISSIONS,
    )
    dependencies = {
        "ioc": ioc,
        "identity_provider": raw_identity_provider,
    }

    app = typer.Typer(
        rich_markup_mode="rich",
        context_settings={"obj": dependencies},
    )
    setup_typer_command_handlers(app)

    return app
