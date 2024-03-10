import asyncio
import os

from faststream import FastStream
from faststream.redis import RedisBroker
from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.presentation.worker.router import router
from amdb.main.providers import (
    ConfigsProvider,
    DomainValidatorsProvider,
    DomainServicesProvider,
    ConnectionsProvider,
    EntityMappersProvider,
    ViewModelMappersProvider,
    ApplicationModelMappersProvider,
    SendingAdaptersProvider,
    TaskQueueAdaptersProvider,
    ConvertingAdaptersProvider,
    PasswordManagerProvider,
    ApllicationServicesProvider,
    CommandHandlersProvider,
    CommandHandlerMakersProvider,
    QueryHandlersProvider,
    QueryHandlerMakersProvider,
)


def run_worker() -> None:
    path_to_config = os.getenv("CONFIG_PATH")
    if not path_to_config:
        message = "Path to config env var is not set"
        raise ValueError(message)

    postgres_config = PostgresConfig.from_toml(path_to_config)
    redis_config = RedisConfig.from_toml(path_to_config)

    broker = RedisBroker(url=redis_config.url)
    broker.include_router(router)

    app = FastStream(broker)
    container = make_async_container(
        ConfigsProvider(
            postgres_config=postgres_config,
            redis_config=redis_config,
        ),
        DomainValidatorsProvider(),
        ConnectionsProvider(),
        DomainServicesProvider(),
        EntityMappersProvider(),
        ViewModelMappersProvider(),
        ApplicationModelMappersProvider(),
        SendingAdaptersProvider(),
        TaskQueueAdaptersProvider(),
        PasswordManagerProvider(),
        ConvertingAdaptersProvider(),
        ApllicationServicesProvider(),
        CommandHandlersProvider(),
        CommandHandlerMakersProvider(),
        QueryHandlersProvider(),
        QueryHandlerMakersProvider(),
    )
    setup_dishka(container, app)

    asyncio.run(app.run())
