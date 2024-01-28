from typing import Annotated

from fastapi import Response, Depends

from amdb.domain.entities.user import UserId
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


async def register(
    ioc: Annotated[HandlerFactory, Depends()],
    session_processor: Annotated[SessionProcessor, Depends(Stub(SessionProcessor))],
    session_gateway: Annotated[RedisSessionGateway, Depends(Stub(RedisSessionGateway))],
    register_user_command: RegisterUserCommand,
    response: Response,
) -> UserId:
    """
    ## Returns: \n
        - user id \n
        - session id in cookies \n

    ## Errors: \n
        - When user name already exists \n
    """
    with ioc.register_user() as register_user_handler:
        user_id = register_user_handler.execute(register_user_command)

    session = session_processor.create(user_id=user_id)
    session_gateway.save(session)

    response.set_cookie(
        key=SESSION_ID_COOKIE,
        value=session.id,
        httponly=True,
    )

    return user_id
