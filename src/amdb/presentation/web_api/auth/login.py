from typing import Annotated
from datetime import datetime, timezone

from fastapi import Response
from dishka.integrations.fastapi import Depends, inject

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
    handler: Annotated[LoginHandler, Depends()],
    session_processor: Annotated[SessionProcessor, Depends()],
    session_mapper: Annotated[SessionMapper, Depends()],
    session_config: Annotated[SessionConfig, Depends()],
    query: LoginQuery,
    response: Response,
) -> UserId:
    """
    Logins, returns user id, creates new authentication session
    and sets cookie with its id. \n\n

    #### Returns 400: \n
        * When user doesn't exist \n
        * When password is incorrect \n
        * When access is denied \n
    """
    user_id = handler.execute(query)

    session = session_processor.create(user_id)
    session_id = session_mapper.save(session)
    session_expires_at = datetime.now(timezone.utc) + session_config.lifetime

    response.set_cookie(
        key=SESSION_ID_COOKIE,
        value=session_id,
        expires=session_expires_at,
        httponly=True,
    )

    return user_id