from unittest.mock import Mock

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import User, UserId
from amdb.domain.services.update_profile import UpdateProfile
from amdb.domain.validators.email import ValidateEmail
from amdb.domain.constants.exceptions import INVALID_EMAIL
from amdb.domain.exception import DomainError
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
        name="JohnDoe",
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
        update_profile=UpdateProfile(validate_email=ValidateEmail()),
        user_gateway=user_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    handler.execute(command)


NOT_EMAIL = "definitelynotemail.com"


def test_update_my_profile_should_raise_error_when_email_is_invalid(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
    )
    user_gateway.save(user)

    unit_of_work.commit()

    identity_provider: IdentityProvider = Mock()
    identity_provider.user_id = Mock(
        return_value=user.id,
    )

    command = UpdateMyProfileCommand(
        email=NOT_EMAIL,
    )
    handler = UpdateMyProfileHandler(
        update_profile=UpdateProfile(validate_email=ValidateEmail()),
        user_gateway=user_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_EMAIL
