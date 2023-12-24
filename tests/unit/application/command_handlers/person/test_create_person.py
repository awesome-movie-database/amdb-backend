from unittest.mock import Mock
from typing import Type
from uuid import UUID, uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import Person
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_person import CreatePerson
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import CREATE_PERSON_ACCESS_DENIED
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_person import CreatePersonCommand
from amdb.application.command_handlers.person.create_person import CreatePersonHandler


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


def test_create_person(
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider_with_valid_access_policy: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    create_person_command = CreatePersonCommand(
        name="John Doe",
        sex=Sex.MALE,
        birth_date=None,
        birth_place=None,
        death_date=None,
        death_place=None,
    )
    creaate_person_handler = CreatePersonHandler(
        access_concern=AccessConcern(),
        create_person=CreatePerson(),
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    person_id = creaate_person_handler.execute(
        command=create_person_command,
    )

    assert isinstance(person_id, UUID)


class TestCreatePersonShouldRaiseCreatePersonAccessDeniedError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        create_person_command = CreatePersonCommand(
            name="John Doe",
            sex=Sex.MALE,
            birth_date=None,
            birth_place=None,
            death_date=None,
            death_place=None,
        )
        creaate_person_handler = CreatePersonHandler(
            access_concern=AccessConcern(),
            create_person=CreatePerson(),
            access_policy_gateway=access_policy_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            creaate_person_handler.execute(
                command=create_person_command,
            )

        assert error.value.messsage == CREATE_PERSON_ACCESS_DENIED
