from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.session import Session, sessionmaker

from .config import DatabaseConfig
from .gateway_factory import GatewayFactory


def build_engine(config: DatabaseConfig) -> Engine:
    return create_engine(url=config.pg_dsn)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine)


class BuildGatewayFactory:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    @contextmanager
    def __call__(self) -> Iterator[GatewayFactory]:
        session = self._session_factory()
        yield GatewayFactory(session)
        session.close()
