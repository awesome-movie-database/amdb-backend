from typing import Annotated, Optional

from fastapi import Cookie, Depends

from amdb.infrastructure.auth.session.gateway import SessionId, SessionGateway
from amdb.infrastructure.auth.session.identity_provider import SessionIdentityProvider
from .depends_stub import Stub


def get_identity_provider(
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    session_id: Annotated[Optional[SessionId], Cookie()],
) -> SessionIdentityProvider:
    return SessionIdentityProvider(
        session_id=session_id,
        session_gateway=session_gateway,
    )
