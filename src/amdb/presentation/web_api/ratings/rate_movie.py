from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.rating import RatingId
from amdb.application.commands.rate_movie import RateMovieCommand
from amdb.application.command_handlers.rate_movie import RateMovieHandler
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerMaker = CreateHandler[RateMovieHandler]


@inject
async def rate_movie(
    *,
    create_handler: Annotated[HandlerMaker, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    command: RateMovieCommand,
) -> RatingId:
    """
    Create movie rating and returns its id. \n\n

    #### Returns 400:
        * When access is denied
        * When movie doesn't exist
        * When rating already exists
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
    handler = create_handler(identity_provider)

    return handler.execute(command)
