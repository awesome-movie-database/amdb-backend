import pytest
from unittest.mock import Mock

from amdb.domain.entities.user.user import User
from amdb.domain.entities.user.profile import Profile
from amdb.domain.services.user.create_user import CreateUser
from amdb.domain.services.user.create_profile import CreateProfile
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.gateways.user.profile import ProfileGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.user.register_user import RegisterUserCommand
from amdb.application.command_handlers.user.register_user import RegisterUserHandler


def test_register_user(
    user: User,
    profile: Profile,
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    create_user: CreateUser = Mock(
        return_value=user,
    )
    create_profile: CreateProfile = Mock(
        return_value=profile,
    )
    user_gateway.check_exists_with_name = Mock(
        return_value=False,
    )

    register_user_command = RegisterUserCommand(
        name=user.name,
        password=user.password,
    )
    register_user_handler = RegisterUserHandler(
        create_user=create_user,
        create_profile=create_profile,
        user_gateway=user_gateway,
        profile_gateway=profile_gateway,
        unit_of_work=unit_of_work,
    )
    user_id = register_user_handler.execute(
        command=register_user_command,
    )

    assert user_id == user.id


def test_register_user_raises_error_when_username_already_exists(
    user: User,
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    create_user: CreateUser = Mock()
    create_profile: CreateProfile = Mock()
    user_gateway.check_exists_with_name = Mock(
        return_value=True,
    )

    register_user_command = RegisterUserCommand(
        name=user.name,
        password=user.password,
    )
    register_user_handler = RegisterUserHandler(
        create_user=create_user,
        create_profile=create_profile,
        user_gateway=user_gateway,
        profile_gateway=profile_gateway,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        register_user_handler.execute(
            command=register_user_command,
        )
    assert error.value.messsage == USER_NAME_ALREADY_EXISTS
