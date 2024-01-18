from typing import Annotated, Optional

from fastapi import Cookie, Depends

from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.infrastructure.auth.session.identity_provider import SessionIdentityProvider
from amdb.infrastructure.auth.session.model import SessionId
from .depends_stub import Stub


def get_identity_provider(
    session_gateway: Annotated[RedisSessionGateway, Depends(Stub(RedisSessionGateway))],
    session_id: Annotated[Optional[SessionId], Cookie()],
) -> SessionIdentityProvider:
    return SessionIdentityProvider(
        session_id=session_id,
        session_gateway=session_gateway,
    )
