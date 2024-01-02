from fastapi import FastAPI

from amdb.infrastructure.auth.session.config import SessionIdentityProviderConfig
from amdb.presentation.web_api.exception_handlers import setup_exception_handlers
from amdb.presentation.web_api.routers.setuper import setup_routers
from amdb.main.config import GenericConfig
from .config import FastAPIConfig
from .di import setup_dependecies


def create_app(
    fastapi_config: FastAPIConfig,
    session_identity_provider_config: SessionIdentityProviderConfig,
    generic_config: GenericConfig,
) -> FastAPI:
    app = FastAPI(
        title=fastapi_config.title,
        summary=fastapi_config.summary,
        description=fastapi_config.description,
        version=fastapi_config.version,
    )
    setup_dependecies(
        app=app,
        session_identity_provider_config=session_identity_provider_config,
        generic_config=generic_config,
    )
    setup_exception_handlers(app)
    setup_routers(app)

    return app
