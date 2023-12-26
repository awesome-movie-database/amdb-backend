from unittest.mock import Mock
from typing import Type
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import MarriageId, Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.delete_marriage import DeleteMarriage
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    DELETE_MARRIAGE_ACCESS_DENIED,
    MARRIAGE_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.delete_marriage import DeleteMarriageCommand
from amdb.application.command_handlers.person.delete_marriage import DeleteMarriageHandler


PersonFactory = Type[DataclassFactory[Person]]
MarriageFactory = Type[DataclassFactory[Marriage]]


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


def test_delete_marriage(
    person_factory: PersonFactory,
    marriage_factory: MarriageFactory,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider_with_valid_access_policy: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    husband = person_factory.build(
        sex=Sex.MALE,
    )
    person_gateway.save(
        person=husband,
    )
    wife = person_factory.build(
        sex=Sex.FEMALE,
    )
    person_gateway.save(
        person=wife,
    )
    marriage = marriage_factory.build(
        husband_id=husband.id,
        wife_id=wife.id,
    )
    marriage_gateway.save(
        marriage=marriage,
    )
    unit_of_work.commit()

    delete_marriage_command = DeleteMarriageCommand(
        marriage_id=marriage.id,
    )
    delete_marriage_handler = DeleteMarriageHandler(
        access_concern=AccessConcern(),
        delete_marriage=DeleteMarriage(),
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    delete_marriage_handler.execute(
        command=delete_marriage_command,
    )


class TestDeleteMarriageShouldRaiseDeleteMarriageAccessDeniedError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        delete_marriage_command = DeleteMarriageCommand(
            marriage_id=MarriageId(uuid4()),
        )
        delete_marriage_handler = DeleteMarriageHandler(
            access_concern=AccessConcern(),
            delete_marriage=DeleteMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            delete_marriage_handler.execute(
                command=delete_marriage_command,
            )

        assert error.value.message == DELETE_MARRIAGE_ACCESS_DENIED


class TestDeleteMarriageShouldRaiseMarriageDoesNotExistError:
    def when_marriage_does_not_exist(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        delete_marriage_command = DeleteMarriageCommand(
            marriage_id=MarriageId(uuid4()),
        )
        delete_marriage_handler = DeleteMarriageHandler(
            access_concern=AccessConcern(),
            delete_marriage=DeleteMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            delete_marriage_handler.execute(
                command=delete_marriage_command,
            )

        assert error.value.message == MARRIAGE_DOES_NOT_EXIST
