from typing import Annotated, Optional

from fastapi import Cookie, Depends

from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.infrastructure.persistence.redis.mappers.permissions import (
    PermissionsMapper,
)
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.infrastructure.auth.session.session import SessionId
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE
from .depends_stub import Stub


def get_identity_provider(
    session_mapper: Annotated[SessionMapper, Depends(Stub(SessionMapper))],
    permissions_mapper: Annotated[
        PermissionsMapper,
        Depends(Stub(PermissionsMapper)),
    ],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
) -> SessionIdentityProvider:
    return SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_mapper,
        permissions_gateway=permissions_mapper,
    )
