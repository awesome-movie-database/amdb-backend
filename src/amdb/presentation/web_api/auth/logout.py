from typing import Annotated, Optional

from fastapi import Response, Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


@inject
async def logout(
    *,
    session_mapper: Annotated[SessionMapper, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    response: Response,
) -> None:
    """
    Logouts and empties session_id cookie. \n\n

    ### Returns 400:
        * When session_id is not set
    """
    if not session_id:
        response.status_code = 400
        return None

    session_mapper.delete_with_id(SessionId(session_id))
    response.set_cookie(
        key="session_id",
        value="",
        httponly=True,
    )

    return None
