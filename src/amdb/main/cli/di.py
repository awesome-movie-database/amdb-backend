from typing import TypedDict
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from amdb.domain.entities.user import UserId
from amdb.infrastructure.permissions_gateway import RawPermissionsGateway
from amdb.infrastructure.auth.raw.identity_provider import RawIdentityProvider
from amdb.infrastructure.security.hasher import Hasher
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC


class DependenciesDict(TypedDict):
    ioc: IoC
    identity_provider: RawIdentityProvider


def create_dependencies_dict(generic_config: GenericConfig) -> DependenciesDict:
    engine = create_engine(generic_config.postgres.dsn)
    ioc = IoC(
        sessionmaker=sessionmaker(engine),
        permissions_gateway=RawPermissionsGateway(),
        hasher=Hasher(),
    )
    identity_provider = RawIdentityProvider(
        user_id=UserId(UUID("00000000-0000-0000-0000-000000000000")),
        permissions=2,
    )

    return DependenciesDict(ioc=ioc, identity_provider=identity_provider)
