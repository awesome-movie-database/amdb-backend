from typing import Annotated

from fastapi import Response, Depends

from amdb.domain.entities.user import UserId
from amdb.application.queries.login import LoginQuery
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.mappers.session import SessionMapper
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


async def login(
    ioc: Annotated[HandlerFactory, Depends()],
    session_processor: Annotated[
        SessionProcessor,
        Depends(Stub(SessionProcessor)),
    ],
    session_mapper: Annotated[SessionMapper, Depends(Stub(SessionMapper))],
    login_query: LoginQuery,
    response: Response,
) -> UserId:
    """
    ## Returns: \n
        - user id \n
        - session id in cookies \n

    ## Errors: \n
        - When access is denied \n
        - When user name doesn't exist \n
        - When password is incorrect \n
    """
    with ioc.login() as login_handler:
        user_id = login_handler.execute(login_query)

    session = session_processor.create(user_id=user_id)
    session_mapper.save(session)

    response.set_cookie(
        key=SESSION_ID_COOKIE,
        value=session.id,
        httponly=True,
    )

    return user_id
