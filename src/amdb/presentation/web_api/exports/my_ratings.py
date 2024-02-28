from typing import Annotated, Optional

from fastapi import Cookie
from fastapi.responses import StreamingResponse
from dishka.integrations.fastapi import Depends, inject

from amdb.application.common.constants.export import ExportFormat
from amdb.application.queries.export_my_ratings import ExportMyRatingsQuery
from amdb.application.query_handlers.export_my_ratings import (
    ExportMyRatingsHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[ExportMyRatingsHandler]


@inject
async def export_my_ratings(
    *,
    create_handler: Annotated[HandlerCreator, Depends()],
    session_gateway: Annotated[SessionGateway, Depends()],
    permissions_gateway: Annotated[PermissionsGateway, Depends()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    format: ExportFormat = ExportFormat.CSV,
):
    """
    Creates file of specified format with current user ratings and
    returns it.
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    query = ExportMyRatingsQuery(format=format)
    file = handler.execute(query)

    if query.format is ExportFormat.CSV:
        media_type = "text/csv"

    response = StreamingResponse(
        content=iter(file),
        media_type=media_type,
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )
    return response
