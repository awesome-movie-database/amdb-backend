from typing import Type
from uuid import UUID

import pytest
from polyfactory.factories import DataclassFactory

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


UserFactory = Type[DataclassFactory[User]]


def test_register_user(
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    register_user_command = RegisterUserCommand(
        name="JohnDoe",
        password="password",
    )
    register_user_handler = RegisterUserHandler(
        create_user=CreateUser(),
        create_profile=CreateProfile(),
        user_gateway=user_gateway,
        profile_gateway=profile_gateway,
        unit_of_work=unit_of_work,
    )

    user_id = register_user_handler.execute(
        command=register_user_command,
    )

    assert isinstance(user_id, UUID)


class TestRegisterUserShouldRaiseUserNameAlreadyExistsError:
    def when_user_name_already_exists(
        self,
        user_factory: UserFactory,
        user_gateway: UserGateway,
        profile_gateway: ProfileGateway,
        unit_of_work: UnitOfWork,
    ) -> None:
        user = user_factory.build()
        user_gateway.save(
            user=user,
        )
        unit_of_work.commit()

        register_user_command = RegisterUserCommand(
            name=user.name,
            password="password",
        )
        register_user_handler = RegisterUserHandler(
            create_user=CreateUser(),
            create_profile=CreateProfile(),
            user_gateway=user_gateway,
            profile_gateway=profile_gateway,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            register_user_handler.execute(
                command=register_user_command,
            )

        assert error.value.message == USER_NAME_ALREADY_EXISTS
