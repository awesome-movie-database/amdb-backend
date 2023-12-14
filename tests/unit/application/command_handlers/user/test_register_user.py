from unittest.mock import Mock

import pytest

from amdb.domain.entities.user.user import User
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
    create_profile: CreateProfile,
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    user_gateway.with_name = Mock(
        return_value=None,
    )
    create_user: CreateUser = Mock(
        return_value=user,
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
    other_user: User,
    create_user: CreateUser,
    create_profile: CreateProfile,
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    other_user.name = user.name
    user_gateway.with_name = Mock(
        return_value=other_user,
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
