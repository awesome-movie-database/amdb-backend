from unittest.mock import Mock

import pytest

from amdb.domain.entities.user.access_policy import AccessPolicyWithIdentity
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.verify_user import VerifyUser
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.user.verify_user import VerifyUserCommand
from amdb.application.command_handlers.user.verify_user import VerifyUserHandler
from amdb.application.common.constants.exceptions import (
    VERIFY_USER_ACCESS_DENIED,
    USER_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


@pytest.mark.usefixtures("clear_database")
def test_verify_user(
    system_user_id: UserId,
    user: User,
    access_concern: AccessConcern,
    verify_user: VerifyUser,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicyWithIdentity(
        is_active=True,
        is_verified=True,
        id=system_user_id,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    user_gateway.save(
        user=user,
    )
    unit_of_work.commit()

    verify_user_command = VerifyUserCommand(
        user_id=user.id,
    )
    verify_user_handler = VerifyUserHandler(
        access_concern=access_concern,
        verify_user=verify_user,
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    verify_user_handler.execute(
        command=verify_user_command,
    )


@pytest.mark.usefixtures("clear_database")
def test_verify_user_raises_error_when_access_is_denied(
    user: User,
    access_concern: AccessConcern,
    verify_user: VerifyUser,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicyWithIdentity(
        is_active=True,
        is_verified=True,
        id=user.id,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    user_gateway.save(
        user=user,
    )
    unit_of_work.commit()

    verify_user_command = VerifyUserCommand(
        user_id=user.id,
    )
    verify_user_handler = VerifyUserHandler(
        access_concern=access_concern,
        verify_user=verify_user,
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        verify_user_handler.execute(
            command=verify_user_command,
        )
    assert error.value.messsage == VERIFY_USER_ACCESS_DENIED


@pytest.mark.usefixtures("clear_database")
def test_verify_user_raises_error_when_user_does_not_exist(
    system_user_id: UserId,
    user: User,
    access_concern: AccessConcern,
    verify_user: VerifyUser,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicyWithIdentity(
        is_active=True,
        is_verified=True,
        id=system_user_id,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )

    verify_user_command = VerifyUserCommand(
        user_id=user.id,
    )
    verify_user_handler = VerifyUserHandler(
        access_concern=access_concern,
        verify_user=verify_user,
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        verify_user_handler.execute(
            command=verify_user_command,
        )
    assert error.value.messsage == USER_DOES_NOT_EXIST
