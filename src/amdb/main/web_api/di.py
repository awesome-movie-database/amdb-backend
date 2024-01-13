from fastapi import FastAPI

from amdb.infrastructure.persistence.sqlalchemy.builders import (
    build_engine,
    build_session_factory,
    BuildGatewayFactory,
)
from amdb.infrastructure.permissions_gateway import InMemoryPermissionsGateway
from amdb.infrastructure.auth.session.gateway import SessionGateway
from amdb.infrastructure.auth.session.builders import build_session_gateway
from amdb.infrastructure.security.hasher import Hasher
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC
from .config import SessionIdentityProviderConfig


def setup_dependecies(
    app: FastAPI,
    session_identity_provider_config: SessionIdentityProviderConfig,
    generic_config: GenericConfig,
) -> None:
    engine = build_engine(generic_config.postgres)
    session_factory = build_session_factory(engine)
    ioc = IoC(
        build_gateway_factory=BuildGatewayFactory(session_factory),
        permissions_gateway=InMemoryPermissionsGateway(),
        hasher=Hasher(),
    )
    app.dependency_overrides[HandlerFactory] = ioc  # type: ignore

    session_gateway = build_session_gateway(
        session_identity_provider_config=session_identity_provider_config,
    )
    app.dependency_overrides[Stub(SessionGateway)] = session_gateway  # type: ignore
