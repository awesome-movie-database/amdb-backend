from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import Depends, inject

from amdb.domain.entities.rating import RatingId
from amdb.application.commands.unrate_movie import UnrateMovieCommand
from amdb.application.command_handlers.unrate_movie import UnrateMovieHandler
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[UnrateMovieHandler]


@inject
async def unrate_movie(
    *,
    create_handler: Annotated[HandlerCreator, Depends()],
    session_gateway: Annotated[SessionGateway, Depends()],
    permissions_gateway: Annotated[PermissionsGateway, Depends()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    rating_id: RatingId,
) -> None:
    """
    Removes movie rating. \n\n

    #### Returns 400:
        * When access is denied
        * When rating doesn't exist
        * When user is not a rating owner
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    command = UnrateMovieCommand(rating_id=rating_id)

    handler.execute(command)
