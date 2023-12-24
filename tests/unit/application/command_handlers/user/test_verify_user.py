from unittest.mock import Mock
from typing import Type
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.verify_user import VerifyUser
from amdb.domain.constants.exceptions import USER_ALREADY_VERIFIED
from amdb.domain.exception import DomainError
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


UserFactory = Type[DataclassFactory[User]]


@pytest.fixture(scope="module")
def identity_provider_with_valid_access_policy(
    system_user_id: UserId,
) -> IdentityProvider:
    valid_access_policy = AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )
    identity_provider = Mock()
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )

    return identity_provider


@pytest.fixture(scope="module")
def identity_provider_with_invalid_access_policy() -> IdentityProvider:
    invalid_access_policy = AccessPolicy(
        id=UserId(uuid4()),
        is_active=True,
        is_verified=True,
    )
    identity_provider = Mock()
    identity_provider.get_access_policy = Mock(
        return_value=invalid_access_policy,
    )

    return identity_provider


def test_verify_user(
    user_factory: UserFactory,
    access_policy_gateway: AccessPolicyGateway,
    user_gateway: UserGateway,
    identity_provider_with_valid_access_policy: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    user = user_factory.build()
    user_gateway.save(
        user=user,
    )
    unit_of_work.commit()

    verify_user_command = VerifyUserCommand(
        user_id=user.id,
    )
    verify_user_handler = VerifyUserHandler(
        access_concern=AccessConcern(),
        verify_user=VerifyUser(),
        access_policy_gateway=access_policy_gateway,
        user_gateway=user_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    verify_user_handler.execute(
        command=verify_user_command,
    )


class TestVerifyUserRaisesVerifyUserAccessDeniedError:
    def when_access_is_denied(
        self,
        user_factory: UserFactory,
        access_policy_gateway: AccessPolicyGateway,
        user_gateway: UserGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        user = user_factory.build()
        user_gateway.save(
            user=user,
        )
        unit_of_work.commit()

        verify_user_command = VerifyUserCommand(
            user_id=user.id,
        )
        verify_user_handler = VerifyUserHandler(
            access_concern=AccessConcern(),
            verify_user=VerifyUser(),
            access_policy_gateway=access_policy_gateway,
            user_gateway=user_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            verify_user_handler.execute(
                command=verify_user_command,
            )

        assert error.value.message == VERIFY_USER_ACCESS_DENIED


class TestVerifyUserRaisesUserDoesNotExistError:
    def when_user_does_not_exist(
        self,
        access_policy_gateway: AccessPolicyGateway,
        user_gateway: UserGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        verify_user_command = VerifyUserCommand(
            user_id=UserId(uuid4()),
        )
        verify_user_handler = VerifyUserHandler(
            access_concern=AccessConcern(),
            verify_user=VerifyUser(),
            access_policy_gateway=access_policy_gateway,
            user_gateway=user_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            verify_user_handler.execute(
                command=verify_user_command,
            )

        assert error.value.message == USER_DOES_NOT_EXIST


class TestVerifyUserShouldRaiseUserAlreadyVerifiedError:
    def when_user_already_verified(
        self,
        user_factory: UserFactory,
        access_policy_gateway: AccessPolicyGateway,
        user_gateway: UserGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        user = user_factory.build(
            is_verified=True,
        )
        user_gateway.save(
            user=user,
        )
        unit_of_work.commit()

        verify_user_command = VerifyUserCommand(
            user_id=user.id,
        )
        verify_user_handler = VerifyUserHandler(
            access_concern=AccessConcern(),
            verify_user=VerifyUser(),
            access_policy_gateway=access_policy_gateway,
            user_gateway=user_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(DomainError) as error:
            verify_user_handler.execute(
                command=verify_user_command,
            )

        assert error.value.message == USER_ALREADY_VERIFIED
