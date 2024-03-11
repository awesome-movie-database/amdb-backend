from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.movie_for_later import MovieForLaterId
from amdb.application.commands.add_to_watchlist import AddToWatchlistCommand
from amdb.application.command_handlers.add_to_watchlist import (
    AddToWatchlistHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerMaker = CreateHandler[AddToWatchlistHandler]


@inject
async def add_movie_to_watchlist(
    *,
    create_handler: Annotated[HandlerMaker, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    command: AddToWatchlistCommand,
) -> MovieForLaterId:
    """
    Add movie to watchlist and returns id of its record. \n\n

    ### Returns 400:
        * When movie doesn't exist
        * When movie already in watchlist
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
    handler = create_handler(identity_provider)

    return handler.execute(command)
