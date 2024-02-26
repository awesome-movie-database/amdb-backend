from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import Depends, inject

from amdb.application.common.view_models.my_detailed_ratings import (
    MyDetailedRatingsViewModel,
)
from amdb.application.queries.my_detailed_ratings import (
    GetMyDetailedRatingsQuery,
)
from amdb.application.query_handlers.my_detailed_ratings import (
    GetMyDetailedRatingsQueryHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[GetMyDetailedRatingsQueryHandler]


@inject
async def get_my_detailed_ratings(
    *,
    create_handler: Annotated[HandlerCreator, Depends()],
    session_gateway: Annotated[SessionGateway, Depends()],
    permissions_gateway: Annotated[PermissionsGateway, Depends()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    limit: int = 100,
    offset: int = 0,
) -> MyDetailedRatingsViewModel:
    """
    Returns current user ratings with movies information and
    rating count.
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    query = GetMyDetailedRatingsQuery(
        limit=limit,
        offset=offset,
    )

    return handler.execute(query)
