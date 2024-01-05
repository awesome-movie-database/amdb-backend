from typing import TypedDict
from uuid import UUID

from amdb.domain.entities.user import UserId
from amdb.infrastructure.database.builders import (
    build_engine,
    build_session_factory,
    BuildGatewayFactory,
)
from amdb.infrastructure.in_memory.permissions_gateway import InMemoryPermissionsGateway
from amdb.infrastructure.auth.raw.identity_provider import RawIdentityProvider
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC


class DependenciesDict(TypedDict):
    ioc: IoC
    identity_provider: RawIdentityProvider


def create_dependencies_dict(generic_config: GenericConfig) -> None:
    engine = build_engine(generic_config.database)
    session_factory = build_session_factory(engine)

    ioc = IoC(
        build_gateway_factory=BuildGatewayFactory(session_factory),
        permissions_gateway=InMemoryPermissionsGateway(),
    )
    identity_provider = RawIdentityProvider(
        user_id=UserId(UUID("00000000-0000-0000-0000-000000000000")),
        permissions=2,
    )

    return DependenciesDict(ioc=ioc, identity_provider=identity_provider)
