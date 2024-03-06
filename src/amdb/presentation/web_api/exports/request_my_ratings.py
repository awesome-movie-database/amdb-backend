from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.application.queries.request_my_ratings_export import (
    RequestMyRatingsExportQuery,
)
from amdb.application.query_handlers.request_my_ratings_export import (
    RequestMyRatingsExportHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[RequestMyRatingsExportHandler]


@inject
async def request_my_ratings_export(
    *,
    create_handler: Annotated[HandlerCreator, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    query: RequestMyRatingsExportQuery,
) -> None:
    """
    Sends file of specified format with current user ratings using
    specified sending method.\n\n

    #### Returns 400:
        * When email sending method was passed and user has no email
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
    handler = create_handler(identity_provider)

    handler.execute(query)
