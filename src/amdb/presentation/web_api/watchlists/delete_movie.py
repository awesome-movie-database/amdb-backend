from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.movie_for_later import MovieForLaterId
from amdb.application.commands.delete_from_watchlist import (
    DeleteFromWatchlistCommand,
)
from amdb.application.command_handlers.delete_from_watchlist import (
    DeleteFromWatchlistHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerMaker = CreateHandler[DeleteFromWatchlistHandler]


@inject
async def delete_movie_from_watchlist(
    *,
    create_handler: Annotated[HandlerMaker, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    movie_for_later_id: MovieForLaterId,
) -> None:
    """
    Deletes movie from watchlist. \n\n

    ### Returns 400:
        * When movie not in watchlist
        * When user is not a watchlist owner
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    command = DeleteFromWatchlistCommand(
        movie_for_later_id=movie_for_later_id,
    )

    handler.execute(command)
