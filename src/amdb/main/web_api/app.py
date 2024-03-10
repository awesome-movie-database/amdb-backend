import os

import uvicorn
from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.presentation.web_api.router import router
from amdb.presentation.web_api.exception_handlers import (
    setup_exception_handlers,
)
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
from .session_adapters_provider import SessionAdaptersProvider


def run_web_api() -> None:
    path_to_config = os.getenv("CONFIG_PATH")
    if not path_to_config:
        message = "Path to config env var is not set"
        raise ValueError(message)

    postgres_config = PostgresConfig.from_toml(path_to_config)
    redis_config = RedisConfig.from_toml(path_to_config)
    session_config = SessionConfig.from_toml(path_to_config)

    app = FastAPI(
        title="Awesome Movie Database",
        version="1.0.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )
    app.include_router(router)
    setup_exception_handlers(app)

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
        SessionAdaptersProvider(
            session_config=session_config,
        ),
    )
    setup_dishka(container, app)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )
