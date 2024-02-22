from fastapi import FastAPI

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.presentation.web_api.exception_handlers import (
    setup_exception_handlers,
)
from amdb.presentation.web_api.routers.setup import setup_routers
from .di import setup_dependecies
from .config import WebAPIConfig


def create_app(
    web_api_config: WebAPIConfig,
    postgres_config: PostgresConfig,
    redis_config: RedisConfig,
    session_config: SessionConfig,
) -> FastAPI:
    app = FastAPI(version=web_api_config.version)
    setup_dependecies(
        app=app,
        session_config=session_config,
        postgres_config=postgres_config,
        redis_config=redis_config,
    )
    setup_exception_handlers(app)
    setup_routers(app)

    return app
