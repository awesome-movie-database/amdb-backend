from uuid import uuid4

import pytest

from amdb.domain.entities.user import UserId, User
from amdb.domain.services.create_user import CreateUser
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.create_user import CreateUserCommand
from amdb.application.command_handlers.create_user import CreateUserHandler
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError


def test_create_user(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    create_user_command = CreateUserCommand(
        name="John Doe",
    )
    create_user_handler = CreateUserHandler(
        create_user=CreateUser(),
        user_gateway=user_gateway,
        unit_of_work=unit_of_work,
    )

    create_user_handler.execute(
        command=create_user_command,
    )


def test_create_user_should_raise_error_when_user_name_already_exists(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    user_name = "John Doe"

    user = User(
        id=UserId(uuid4()),
        name=user_name,
    )
    user_gateway.save(user)
    unit_of_work.commit()

    create_user_command = CreateUserCommand(
        name=user_name,
    )
    create_user_handler = CreateUserHandler(
        create_user=CreateUser(),
        user_gateway=user_gateway,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_user_handler.execute(
            command=create_user_command,
        )
    
    assert error.value.message == USER_NAME_ALREADY_EXISTS
