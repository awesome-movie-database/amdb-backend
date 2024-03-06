from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.review import ReviewId
from amdb.application.commands.review_movie import ReviewMovieCommand
from amdb.application.command_handlers.review_movie import ReviewMovieHandler
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerCreator = CreateHandler[ReviewMovieHandler]


@inject
async def review_movie(
    *,
    create_handler: Annotated[HandlerCreator, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    command: ReviewMovieCommand,
) -> ReviewId:
    """
    Create movie review and returns its id.\n\n

    #### Returns 400:
        * When access is denied
        * When movie doesn't exist
        * When review already exists
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )
    handler = create_handler(identity_provider)

    return handler.execute(command)
