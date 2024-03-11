from typing import Annotated
from datetime import datetime, timezone

from fastapi import Response
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.user import UserId
from amdb.application.queries.login import LoginQuery
from amdb.application.query_handlers.login import LoginHandler
from amdb.infrastructure.auth.session.config import SessionConfig
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


@inject
async def login(
    *,
    handler: Annotated[LoginHandler, FromDishka()],
    session_processor: Annotated[SessionProcessor, FromDishka()],
    session_mapper: Annotated[SessionMapper, FromDishka()],
    session_config: Annotated[SessionConfig, FromDishka()],
    query: LoginQuery,
    response: Response,
) -> UserId:
    """
    Logins, returns user id, creates new authentication session
    and sets cookie with its id. \n\n

    #### Returns 400:
        * When user doesn't exist
        * When password is incorrect
        * When access is denied
    """
    user_id = handler.execute(query)

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
