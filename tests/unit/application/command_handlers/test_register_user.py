import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.services.create_user import CreateUser
from amdb.domain.validators.email import ValidateEmail
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.password_manager import PasswordManager
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.common.constants.exceptions import (
    USER_NAME_ALREADY_EXISTS,
    USER_EMAIL_ALREADY_EXISTS,
)
from amdb.application.common.exception import ApplicationError


def test_register_user(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    command = RegisterUserCommand(
        name="JohnDoe",
        email="John@doe.com",
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(validate_email=ValidateEmail()),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    handler.execute(command)


def test_create_user_should_raise_error_when_user_name_already_exists(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    user_name = "JohnDoe"

    user = User(
        id=UserId(uuid7()),
        name=user_name,
        email="John@doe.com",
    )
    user_gateway.save(user)

    unit_of_work.commit()

    command = RegisterUserCommand(
        name=user_name,
        email=None,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(validate_email=ValidateEmail()),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_NAME_ALREADY_EXISTS


def test_create_user_should_raise_error_when_user_email_already_exists(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    user_email = "John@doe.com"

    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email=user_email,
    )
    user_gateway.save(user)

    unit_of_work.commit()

    command = RegisterUserCommand(
        name="JohnyDoe",
        email=user_email,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(validate_email=ValidateEmail()),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_EMAIL_ALREADY_EXISTS
