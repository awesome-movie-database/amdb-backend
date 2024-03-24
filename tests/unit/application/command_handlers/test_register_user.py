import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.services.create_user import CreateUser
from amdb.domain.validators.email import ValidateEmail
from amdb.domain.validators.telegram import ValidateTelegram
from amdb.domain.constants.exceptions import (
    INVALID_USER_NAME,
    INVALID_EMAIL,
    INVALID_TELEGRAM,
)
from amdb.domain.exception import DomainError
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.password_manager import PasswordManager
from amdb.application.commands.register_user import RegisterUserCommand
from amdb.application.command_handlers.register_user import RegisterUserHandler
from amdb.application.common.constants.exceptions import (
    USER_NAME_ALREADY_EXISTS,
    USER_EMAIL_ALREADY_EXISTS,
    USER_TELEGRAM_ALREADY_EXISTS,
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
        telegram="johndoe",
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    handler.execute(command)


def test_register_user_should_raise_error_when_user_name_already_exists(
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
        telegram=None,
    )
    user_gateway.save(user)

    unit_of_work.commit()

    command = RegisterUserCommand(
        name=user_name,
        email=None,
        telegram=None,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_NAME_ALREADY_EXISTS


def test_register_user_should_raise_error_when_user_email_already_exists(
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
        telegram=None,
    )
    user_gateway.save(user)

    unit_of_work.commit()

    command = RegisterUserCommand(
        name="JohnyDoe",
        email=user_email,
        telegram="johndoe",
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_EMAIL_ALREADY_EXISTS


def test_register_user_should_raise_error_when_user_telegram_already_exists(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    user_telegram = "johndoe"

    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email=None,
        telegram=user_telegram,
    )
    user_gateway.save(user)

    unit_of_work.commit()

    command = RegisterUserCommand(
        name="JohnyDoe",
        email=None,
        telegram=user_telegram,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == USER_TELEGRAM_ALREADY_EXISTS


USER_NAME_SHORTER_THAN_1_CHARACTER = ""
USER_NAME_LONGER_THAN_128_CHARACTERS = "_" * 129


@pytest.mark.parametrize(
    "user_name",
    (
        USER_NAME_SHORTER_THAN_1_CHARACTER,
        USER_NAME_LONGER_THAN_128_CHARACTERS,
    ),
)
def test_register_user_should_raise_error_when_name_is_invalid(
    user_name: str,
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    command = RegisterUserCommand(
        name=user_name,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_USER_NAME


NOT_EMAIL = "definitelynotemail.com"


def test_register_user_should_raise_error_when_email_is_invalid(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    command = RegisterUserCommand(
        name="JohnDoe",
        email=NOT_EMAIL,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_EMAIL


NOT_TELEGRAM = "definitely not telegram"


def test_register_user_should_raise_error_when_telegram_is_invalid(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    unit_of_work: UnitOfWork,
    password_manager: PasswordManager,
):
    command = RegisterUserCommand(
        name="JohnDoe",
        telegram=NOT_TELEGRAM,
        password="Secret",
    )
    handler = RegisterUserHandler(
        create_user=CreateUser(
            validate_email=ValidateEmail(),
            validate_telegram=ValidateTelegram(),
        ),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        unit_of_work=unit_of_work,
        password_manager=password_manager,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_TELEGRAM
