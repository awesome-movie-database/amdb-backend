import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.services.create_user import CreateUser
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.password_manager import PasswordManager
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError


def test_register_user(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    register_user_command = RegisterUserCommand(
        name="John Doe",
        password="Secret",
    )
    register_user_handler = RegisterUserHandler(
        create_user=CreateUser(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    register_user_handler.execute(register_user_command)


def test_create_user_should_raise_error_when_user_name_already_exists(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    user_name = "John Doe"

    user = User(
        id=UserId(uuid7()),
        name=user_name,
    )
    user_gateway.save(user)
    unit_of_work.commit()

    register_user_command = RegisterUserCommand(
        name=user_name,
        password="Secret",
    )
    register_user_handler = RegisterUserHandler(
        create_user=CreateUser(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        register_user_handler.execute(register_user_command)

    assert error.value.message == USER_NAME_ALREADY_EXISTS
