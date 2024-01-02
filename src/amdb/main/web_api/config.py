import os
from dataclasses import dataclass
from datetime import timedelta

from amdb.infrastructure.auth.session.config import SessionIdentityProviderConfig


FASTAPI_TITLE_ENV = "FASTAPI_TITLE"
FASTAPI_SUMMARY_ENV = "FASTAPI_SUMMARY"
FASTAPI_DESCRIPTION_ENV = "FASTAPI_DESCRIPTION"
FASTAPI_VERSION_ENV = "FASTAPI_VERSION"

UVICORN_HOST_ENV = "UVICORN_HOST"
UVICORN_PORT_ENV = "UVICORN_PORT"

SESSION_IDENTITY_PROVIDER_REDIS_HOST_ENV = "SESSION_IDENTITY_PROVIDER_REDIS_HOST"
SESSION_IDENTITY_PROVIDER_REDIS_PORT_ENV = "SESSION_IDENTITY_PROVIDER_REDIS_PORT"
SESSION_IDENTITY_PROVIDER_REDIS_DB_ENV = "SESSION_IDENTITY_PROVIDER_REDIS_DB"
SESSION_IDENTITY_PROVIDER_REDIS_PASSWORD_ENV = "SESSION_IDENTITY_PROVIDER_REDIS_PASSWORD"
SESSION_IDENTITY_PROVIDER_SESSION_LIFETIME_ENV = "SESSION_IDENTITY_PROVIDER_SESSION_LIFETIME"


def build_web_api_config() -> "WebAPIConfig":
    fastapi_config = FastAPIConfig(
        title=_get_env(FASTAPI_TITLE_ENV),
        summary=_get_env(FASTAPI_SUMMARY_ENV),
        description=_get_env(FASTAPI_DESCRIPTION_ENV),
        version=_get_env(FASTAPI_VERSION_ENV),
    )
    uvicorn_config = UvicornConfig(
        host=_get_env(UVICORN_HOST_ENV),
        port=int(_get_env(UVICORN_PORT_ENV)),
    )
    session_identity_provider_config = SessionIdentityProviderConfig(
        redis_host=_get_env(SESSION_IDENTITY_PROVIDER_REDIS_HOST_ENV),
        redis_port=int(_get_env(SESSION_IDENTITY_PROVIDER_REDIS_PORT_ENV)),
        redis_db=int(_get_env(SESSION_IDENTITY_PROVIDER_REDIS_DB_ENV)),
        redis_password=_get_env(SESSION_IDENTITY_PROVIDER_REDIS_PASSWORD_ENV),
        session_lifetime=timedelta(minutes=int(_get_env(SESSION_IDENTITY_PROVIDER_SESSION_LIFETIME_ENV))),
    )
    return WebAPIConfig(
        fastapi=fastapi_config,
        uvicorn=uvicorn_config,
        session_identity_provider=session_identity_provider_config,
    )


def _get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        message = f"Env variable {key} is not set"
        raise ValueError(message)
    return value


@dataclass(frozen=True, slots=True)
class FastAPIConfig:
    title: str
    summary: str
    description: str
    version: str


@dataclass(frozen=True, slots=True)
class UvicornConfig:
    host: str
    port: int


@dataclass(frozen=True, slots=True)
class WebAPIConfig:
    fastapi: FastAPIConfig
    uvicorn: UvicornConfig
    session_identity_provider: SessionIdentityProviderConfig
