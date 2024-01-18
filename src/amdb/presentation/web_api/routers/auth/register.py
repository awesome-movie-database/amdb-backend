from typing import Annotated

from fastapi import Response, Depends
from pydantic import BaseModel

from amdb.domain.entities.user import UserId
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.infrastructure.auth.session.session_processor import SessionProcessor
from amdb.infrastructure.persistence.redis.gateways.session import RedisSessionGateway
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub


class RegisterSchema(BaseModel):
    name: str
    password: str


async def register(
    ioc: Annotated[HandlerFactory, Depends()],
    session_processor: Annotated[SessionProcessor, Depends(Stub(SessionProcessor))],
    session_gateway: Annotated[RedisSessionGateway, Depends(Stub(RedisSessionGateway))],
    data: RegisterSchema,
    response: Response,
) -> UserId:
    with ioc.register_user() as register_user_handler:
        register_user_command = RegisterUserCommand(
            name=data.name,
            password=data.password,
        )
        user_id = register_user_handler.execute(register_user_command)

    session = session_processor.create(user_id=user_id, permissions=4)
    session_gateway.save(session)

    response.set_cookie(
        key="session_id",
        value=session.id,
        httponly=True,
        secure=True,
    )

    return user_id
