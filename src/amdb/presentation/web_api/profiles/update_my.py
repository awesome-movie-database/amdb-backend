from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import Depends, inject
from amdb.application.commands.update_my_profile import UpdateMyProfileCommand
from amdb.application.command_handlers.update_my_profile import (
    UpdateMyProfileHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[UpdateMyProfileHandler]


@inject
async def update_my_profile(
    *,
    create_handler: Annotated[HandlerCreator, Depends()],
    session_gateway: Annotated[SessionGateway, Depends()],
    permissions_gateway: Annotated[PermissionsGateway, Depends()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    command: UpdateMyProfileCommand,
) -> None:
    """
    Updates current user profile
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
    handler = create_handler(identity_provider)

    handler.execute(command)
