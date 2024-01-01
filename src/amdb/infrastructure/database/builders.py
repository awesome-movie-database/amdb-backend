from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.session import Session, sessionmaker

from .config import DatabaseConfig
from .gateway_factory import GatewayFactory


def build_engine(config: DatabaseConfig) -> Engine:
    return create_engine(url=config.pg_dsn)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine)


def build_gateway_factory(session: Session) -> GatewayFactory:
    return GatewayFactory(session)
