from unittest.mock import Mock

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import User
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.update_user import UpdateUser
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.commands.user.update_user import UpdateUserCommand
from amdb.application.command_handlers.user.update_user import UpdateUserHandler
from amdb.application.common.constants.exceptions import UPDATE_USER_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError


@pytest.mark.usefixtures("clear_database")
def test_update_user(
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    user_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=User,
    )
    user = user_factory.build(
        name="John Doe",
    )
    current_access_policy = AccessPolicy(
        id=user.id,
        is_active=True,
        is_verified=False,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    user_gateway.save(
        user=user,
    )
    unit_of_work.commit()
    update_user_command = UpdateUserCommand(
        name="Johny Doe",
    )
    update_user_handler = UpdateUserHandler(
        access_concern=AccessConcern(),
        update_user=UpdateUser(),
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    update_user_handler.execute(
        command=update_user_command,
    )


@pytest.mark.usefixtures("clear_database")
def test_update_user_raises_error_when_access_is_denied(
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    user_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=User,
    )
    user = user_factory.build()
    current_access_policy = AccessPolicy(
        id=user.id,
        is_active=False,
        is_verified=False,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    user_gateway.save(
        user=user,
    )
    unit_of_work.commit()
    update_user_command = UpdateUserCommand(
        name=user.name,
    )
    update_user_handler = UpdateUserHandler(
        access_concern=AccessConcern(),
        update_user=UpdateUser(),
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        update_user_handler.execute(
            command=update_user_command,
        )

    assert error.value.messsage == UPDATE_USER_ACCESS_DENIED
