from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from redis.client import Redis

from amdb.infrastructure.permissions_gateway import RawPermissionsGateway
from amdb.infrastructure.security.hasher import Hasher
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.main.config import GenericConfig
from amdb.main.ioc import IoC


def setup_dependecies(
    app: FastAPI,
    redis_config: RedisConfig,
    session_config: SessionConfig,
    generic_config: GenericConfig,
) -> None:
    hasher = Hasher()

    engine = create_engine(generic_config.postgres.dsn)
    ioc = IoC(
        sessionmaker=sessionmaker(engine),
        permissions_gateway=RawPermissionsGateway(),
        hasher=hasher,
    )
    app.dependency_overrides[HandlerFactory] = lambda: ioc  # type: ignore

    redis = Redis(
        host=redis_config.host,
        port=redis_config.port,
        db=redis_config.db,
        password=redis_config.password,
    )
    redis_session_gateway = RedisSessionGateway(
        redis=redis,
        session_lifetime=session_config.session_lifetime,
    )
    app.dependency_overrides[Stub(RedisSessionGateway)] = lambda: redis_session_gateway  # type: ignore

    session_processor = SessionProcessor(hasher=hasher)
    app.dependency_overrides[Stub(SessionProcessor)] = lambda: session_processor  # type: ignore
