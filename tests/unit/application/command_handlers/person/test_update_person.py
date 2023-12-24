from unittest.mock import Mock
from typing import Type
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.update_person import UpdatePerson
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    UPDATE_PERSON_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.update_person import UpdatePersonCommand
from amdb.application.command_handlers.person.update_person import UpdatePersonHandler


PersonFactory = Type[DataclassFactory[Person]]


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


def test_update_person(
    person_factory: PersonFactory,
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider_with_valid_access_policy: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person = person_factory.build(
        name="John Doe",
    )
    person_gateway.save(
        person=person,
    )
    unit_of_work.commit()

    update_person_command = UpdatePersonCommand(
        person_id=person.id,
        name="Johny Doe",
    )
    update_person_handler = UpdatePersonHandler(
        access_concern=AccessConcern(),
        update_person=UpdatePerson(),
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    update_person_handler.execute(
        command=update_person_command,
    )


class TestUpdateUserShouldRaiseUpdatePersonAccessDeniedError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        update_person_command = UpdatePersonCommand(
            person_id=PersonId(uuid4()),
            name="John Doe",
        )
        update_person_handler = UpdatePersonHandler(
            access_concern=AccessConcern(),
            update_person=UpdatePerson(),
            access_policy_gateway=access_policy_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_person_handler.execute(
                command=update_person_command,
            )

        assert error.value.messsage == UPDATE_PERSON_ACCESS_DENIED


class TestUpdateUserShouldRaisePersonDoesNotExistError:
    def when_person_does_not_exist(
        self,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        update_person_command = UpdatePersonCommand(
            person_id=PersonId(uuid4()),
            name="John Doe",
        )
        update_person_handler = UpdatePersonHandler(
            access_concern=AccessConcern(),
            update_person=UpdatePerson(),
            access_policy_gateway=access_policy_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_person_handler.execute(
                command=update_person_command,
            )

        assert error.value.messsage == PERSON_DOES_NOT_EXIST
