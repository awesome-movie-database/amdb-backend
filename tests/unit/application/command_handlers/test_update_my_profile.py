from unittest.mock import Mock

from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.services.update_profile import UpdateProfile
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.update_my_profile import UpdateMyProfileCommand
from amdb.application.command_handlers.update_my_profile import (
    UpdateMyProfileHandler,
)


def test_update_my_profile(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
        email="John@doe.com",
    )
    user_gateway.save(user)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(
        return_value=user.id,
    )

    command = UpdateMyProfileCommand(
        email="Johny@doe.com",
    )
    handler = UpdateMyProfileHandler(
        update_profile=UpdateProfile(),
        user_gateway=user_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    handler.execute(command)
