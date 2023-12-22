from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import sessionmaker, Session

from .gateway_factory import GatewayFactory


def build_engine(
    *,
    url: str,
) -> Engine:
    return create_engine(
        url=url,
        echo=True,
    )


def build_session_factory(
    *,
    engine: Engine,
) -> sessionmaker[Session]:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


def build_gateway_factory(
    *,
    session: Session,
) -> GatewayFactory:
    return GatewayFactory(
        session=session,
    )
