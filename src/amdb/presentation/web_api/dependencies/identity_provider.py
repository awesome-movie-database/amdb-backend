from typing import Annotated, Optional

from fastapi import Cookie, Depends

from amdb.infrastructure.persistence.redis.gateways.session import (
    RedisSessionGateway,
)
from amdb.infrastructure.persistence.redis.gateways.permissions import (
    RedisPermissionsGateway,
)
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.infrastructure.auth.session.model import SessionId
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE
from .depends_stub import Stub


def get_identity_provider(
    session_gateway: Annotated[
        RedisSessionGateway, Depends(Stub(RedisSessionGateway))
    ],
    permissions_gateway: Annotated[
        RedisPermissionsGateway,
        Depends(Stub(RedisPermissionsGateway)),
    ],
    session_id: Annotated[
        Optional[str], Cookie(alias=SESSION_ID_COOKIE)
    ] = None,
) -> SessionIdentityProvider:
    return SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
