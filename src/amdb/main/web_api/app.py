from fastapi import FastAPI

from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.presentation.web_api.exception_handlers import setup_exception_handlers
from amdb.presentation.web_api.routers.setup import setup_routers
from amdb.main.config import GenericConfig
from .config import FastAPIConfig
from .di import setup_dependecies


def create_app(
    fastapi_config: FastAPIConfig,
    redis_config: RedisConfig,
    session_config: SessionConfig,
    generic_config: GenericConfig,
) -> FastAPI:
    app = FastAPI(version=fastapi_config.version)
    setup_dependecies(
        app=app,
        redis_config=redis_config,
        session_config=session_config,
        generic_config=generic_config,
    )
    setup_exception_handlers(app)
    setup_routers(app)

    return app
