from typing import Annotated
from datetime import datetime, timezone

from fastapi import Response
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.user import UserId
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


@inject
async def register(
    *,
    handler: Annotated[RegisterUserHandler, FromDishka()],
    session_processor: Annotated[SessionProcessor, FromDishka()],
    session_mapper: Annotated[SessionMapper, FromDishka()],
    session_config: Annotated[SessionConfig, FromDishka()],
    command: RegisterUserCommand,
    response: Response,
) -> UserId:
    """
    Registers user, returns his id, creates new
    authentication session and sets cookie with its id. \n\n

    #### Returns 400:
        * When name is already taken
    """
    user_id = handler.execute(command)

    session = session_processor.create(user_id)
    session_mapper.save(session)
    session_expires_at = datetime.now(timezone.utc) + session_config.lifetime

    response.set_cookie(
        key=SESSION_ID_COOKIE,
        value=session.id,
        expires=session_expires_at,
        httponly=True,
    )

    return user_id
