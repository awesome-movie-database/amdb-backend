from unittest.mock import Mock
from typing import Type
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import MarriageId, MarriageStatus, Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.update_marriage import UpdateMarriage
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.exception import ApplicationError
from amdb.application.common.constants.exceptions import (
    UPDATE_MARRIAGE_INVALID_COMMAND,
    UPDATE_MARRIAGE_ACCESS_DENIED,
    MARRIAGE_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
)
from amdb.application.commands.person.update_marriage import UpdateMarriageCommand
from amdb.application.command_handlers.person.update_marriage import UpdateMarriageHandler


PersonFactory = Type[DataclassFactory[Person]]
MarriageFactory = Type[DataclassFactory[Marriage]]

HUSBAND_ID = PersonId(uuid4())
WIFE_ID = PersonId(uuid4())


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


def test_update_marriage(
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
    old_child = person_factory.build()
    person_gateway.save(
        person=old_child,
    )
    marriage = marriage_factory.build(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[old_child.id],
    )
    marriage_gateway.save(
        marriage=marriage,
    )
    new_child = person_factory.build()
    person_gateway.save(
        person=new_child,
    )
    unit_of_work.commit()

    update_marriage_command = UpdateMarriageCommand(
        marriage_id=marriage.id,
        child_ids=[new_child.id],
    )
    update_marriage_handler = UpdateMarriageHandler(
        access_concern=AccessConcern(),
        update_marriage=UpdateMarriage(),
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    update_marriage_handler.execute(
        command=update_marriage_command,
    )


class TestUpdateMarriageShouldRaiseUpdateMarriageError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        update_marriage_command = UpdateMarriageCommand(
            marriage_id=MarriageId(uuid4()),
            status=MarriageStatus.HE_FILED_FOR_DIVORCE,
        )
        update_marriage_handler = UpdateMarriageHandler(
            access_concern=AccessConcern(),
            update_marriage=UpdateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_marriage_handler.execute(
                command=update_marriage_command,
            )

        assert error.value.message == UPDATE_MARRIAGE_ACCESS_DENIED


class TestUpdateMarriageShouldRaiseUpdateMarriageInvalidCommandError:
    @pytest.mark.parametrize(
        argnames=(
            "husband_id",
            "wife_id",
            "child_ids",
        ),
        argvalues=(
            (
                HUSBAND_ID,
                WIFE_ID,
                [HUSBAND_ID],
            ),
            (
                HUSBAND_ID,
                WIFE_ID,
                [WIFE_ID],
            ),
        ),
    )
    def when_husband_or_wife_ids_passed_to_child_ids(
        self,
        husband_id: PersonId,
        wife_id: PersonId,
        child_ids: list[PersonId],
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        husband = person_factory.build(
            id=husband_id,
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=husband,
        )
        wife = person_factory.build(
            id=wife_id,
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

        update_marriage_command = UpdateMarriageCommand(
            marriage_id=marriage.id,
            child_ids=child_ids,
        )
        update_marriage_handler = UpdateMarriageHandler(
            access_concern=AccessConcern(),
            update_marriage=UpdateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_marriage_handler.execute(
                command=update_marriage_command,
            )

        assert error.value.message == UPDATE_MARRIAGE_INVALID_COMMAND


class TestUpdateMarriageShouldRaiseMarriageDoesNotExistError:
    def when_marriage_does_not_exist(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        update_marriage_command = UpdateMarriageCommand(
            marriage_id=MarriageId(uuid4()),
            status=MarriageStatus.HE_FILED_FOR_DIVORCE,
        )
        update_marriage_handler = UpdateMarriageHandler(
            access_concern=AccessConcern(),
            update_marriage=UpdateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_marriage_handler.execute(
                command=update_marriage_command,
            )

        assert error.value.message == MARRIAGE_DOES_NOT_EXIST


class TestUpdateMarriageShouldRaisePersonsDoNotExistError:
    def when_children_do_not_exist(
        self,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        nonexistent_child_ids = [
            PersonId(uuid4()),
            PersonId(uuid4()),
            PersonId(uuid4()),
        ]

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

        update_marriage_command = UpdateMarriageCommand(
            marriage_id=marriage.id,
            child_ids=nonexistent_child_ids,
        )
        update_marriage_handler = UpdateMarriageHandler(
            access_concern=AccessConcern(),
            update_marriage=UpdateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            update_marriage_handler.execute(
                command=update_marriage_command,
            )

        assert error.value.message == PERSONS_DO_NOT_EXIST
