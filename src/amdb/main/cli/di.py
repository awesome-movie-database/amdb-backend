from typing import TypedDict
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from redis.client import Redis

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.redis.gateways.permissions import RedisPermissionsGateway
from amdb.infrastructure.auth.raw.identity_provider import RawIdentityProvider
from amdb.infrastructure.security.hasher import Hasher
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC


IDENTITY_PROVIDER_USER_ID = UserId(UUID("00000000-0000-0000-0000-000000000000"))
IDENTITY_PROVIDER_PERMISSIONS = 12


class DependenciesDict(TypedDict):
    ioc: IoC
    identity_provider: RawIdentityProvider


def create_dependencies_dict(generic_config: GenericConfig) -> DependenciesDict:
    redis = Redis(
        host=generic_config.redis.host,
        port=generic_config.redis.port,
        db=generic_config.redis.db,
        password=generic_config.redis.password,
    )
    engine = create_engine(generic_config.postgres.dsn)
    ioc = IoC(
        sessionmaker=sessionmaker(engine),
        permissions_gateway=RedisPermissionsGateway(redis),
        hasher=Hasher(),
    )
    identity_provider = RawIdentityProvider(
        user_id=IDENTITY_PROVIDER_USER_ID,
        permissions=IDENTITY_PROVIDER_PERMISSIONS,
    )

    return DependenciesDict(ioc=ioc, identity_provider=identity_provider)
