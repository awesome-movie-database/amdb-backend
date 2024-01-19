from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from redis.client import Redis

from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.infrastructure.persistence.redis.gateways.permissions import RedisPermissionsGateway
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC


def setup_dependecies(
    app: FastAPI,
    session_config: SessionConfig,
    generic_config: GenericConfig,
) -> None:
    redis = Redis(
        host=generic_config.redis.host,
        port=generic_config.redis.port,
        db=generic_config.redis.db,
        password=generic_config.redis.password,
    )
    redis_session_gateway = RedisSessionGateway(
        redis=redis,
        session_lifetime=session_config.session_lifetime,
    )
    app.dependency_overrides[Stub(RedisSessionGateway)] = lambda: redis_session_gateway  # type: ignore

    redis_permissions_gateway = RedisPermissionsGateway(redis)
    app.dependency_overrides[Stub(RedisPermissionsGateway)] = lambda: redis_permissions_gateway  # type: ignore

    engine = create_engine(generic_config.postgres.dsn)
    ioc = IoC(
        sessionmaker=sessionmaker(engine),
        permissions_gateway=redis_permissions_gateway,
        hasher=Hasher(),
    )
    app.dependency_overrides[HandlerFactory] = lambda: ioc  # type: ignore

    session_processor = SessionProcessor(hasher=Hasher())
    app.dependency_overrides[Stub(SessionProcessor)] = lambda: session_processor  # type: ignore
