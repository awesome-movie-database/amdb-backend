from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from amdb.domain.entities.user import UserId
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.infrastructure.auth.session.gateway import Session, SessionGateway
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.depends_stub import Stub


class RegisterSchema(BaseModel):
    name: str
    password: str


async def register(
    ioc: Annotated[HandlerFactory, Depends()],
    session_gateway: Annotated[SessionGateway, Depends(Stub(SessionGateway))],
    data: RegisterSchema,
) -> UserId:
    with ioc.register_user() as register_user_handler:
        register_user_command = RegisterUserCommand(
            name=data.name,
            password=data.password,
        )
        user_id = register_user_handler.execute(register_user_command)

    session = Session(user_id=user_id, permissions=4)
    session_gateway.save_session(session)

    return user_id
