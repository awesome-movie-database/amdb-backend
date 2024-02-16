import os
from dataclasses import dataclass
from datetime import timedelta

from amdb.infrastructure.auth.session.config import SessionConfig


FASTAPI_VERSION_ENV = "FASTAPI_VERSION"

UVICORN_HOST_ENV = "UVICORN_HOST"
UVICORN_PORT_ENV = "UVICORN_PORT"

SESSION_LIFETIME_ENV = "SESSION_LIFETIME"


def build_web_api_config() -> "WebAPIConfig":
    fastapi_config = FastAPIConfig(
        version=_get_env(FASTAPI_VERSION_ENV),
    )
    uvicorn_config = UvicornConfig(
        host=_get_env(UVICORN_HOST_ENV),
        port=int(_get_env(UVICORN_PORT_ENV)),
    )
    session_config = SessionConfig(
        session_lifetime=timedelta(
            minutes=int(_get_env(SESSION_LIFETIME_ENV))
        ),
    )
    return WebAPIConfig(
        fastapi=fastapi_config,
        uvicorn=uvicorn_config,
        session=session_config,
    )


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@dataclass(frozen=True, slots=True)
class FastAPIConfig:
    version: str


@dataclass(frozen=True, slots=True)
class UvicornConfig:
    host: str
    port: int


@dataclass(frozen=True, slots=True)
class WebAPIConfig:
    fastapi: FastAPIConfig
    uvicorn: UvicornConfig
    session: SessionConfig
