from unittest.mock import Mock
from typing import Type
from uuid import UUID, uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import MarriageStatus, Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.domain.constants.exceptions import PERSONS_HAVE_SAME_SEX
from amdb.domain.exception import DomainError
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_MARRIAGE_INVALID_COMMAND,
    CREATE_MARRIAGE_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
    PERSON_IS_MARRIED,
    MARRIAGE_ALREADY_EXISTS,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_marriage import CreateMarriageCommand
from amdb.application.command_handlers.person.create_marriage import CreateMarriageHandler


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


def test_create_marriage(
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
    child = person_factory.build()
    person_gateway.save(
        person=child,
    )
    marriage = marriage_factory.build(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[child.id],
    )
    unit_of_work.commit()

    create_marriage_command = CreateMarriageCommand(
        husband_id=marriage.husband_id,
        wife_id=marriage.wife_id,
        child_ids=marriage.child_ids,
        status=marriage.status,
        start_date=marriage.start_date,
        end_date=marriage.end_date,
    )
    create_marriage_handler = CreateMarriageHandler(
        access_concern=AccessConcern(),
        create_marriage=CreateMarriage(),
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    marriage_id = create_marriage_handler.execute(
        command=create_marriage_command,
    )

    assert isinstance(marriage_id, UUID)


class TestCreateMarriageShouldRaiseCreateMarriageAccessDeniedError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        create_marriage_command = CreateMarriageCommand(
            husband_id=PersonId(uuid4()),
            wife_id=PersonId(uuid4()),
            child_ids=[],
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == CREATE_MARRIAGE_ACCESS_DENIED


class TestCreateMarriageShouldRaiseCreatePersonInvalidCommandError:
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
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband_id,
            wife_id=wife_id,
            child_ids=child_ids,
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == CREATE_MARRIAGE_INVALID_COMMAND


class TestCreateMarriageShouldRaisePersonsDoNotExist:
    def when_children_do_not_exist(
        self,
        person_factory: PersonFactory,
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
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband.id,
            wife_id=wife.id,
            child_ids=nonexistent_child_ids,
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSONS_DO_NOT_EXIST
        assert all(
            (
                nonexistent_child_id in error.value.extra["person_ids"]
                for nonexistent_child_id in nonexistent_child_ids
            ),
        )


class TestCreateMarriageShouldRaisePersonDoesNotExistError:
    def when_husband_does_not_exist(
        self,
        person_factory: PersonFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        nonexistent_husband_id = PersonId(uuid4())

        wife = person_factory.build(
            sex=Sex.FEMALE,
        )
        person_gateway.save(
            person=wife,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=nonexistent_husband_id,
            wife_id=wife.id,
            child_ids=[],
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSON_DOES_NOT_EXIST
        assert error.value.extra["person_id"] == nonexistent_husband_id

    def when_wife_does_not_exist(
        self,
        person_factory: PersonFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        nonexistent_wife_id = PersonId(uuid4())

        husband = person_factory.build(
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=husband,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband.id,
            wife_id=nonexistent_wife_id,
            child_ids=[],
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSON_DOES_NOT_EXIST
        assert error.value.extra["person_id"] == nonexistent_wife_id


class TestCreateMarriageShouldRaisePersonsHaveSameSexError:
    @pytest.mark.parametrize(
        argnames=(
            "husband_sex",
            "wife_sex",
        ),
        argvalues=(
            (
                Sex.MALE,
                Sex.MALE,
            ),
            (
                Sex.FEMALE,
                Sex.FEMALE,
            ),
        ),
    )
    def when_husband_and_wife_have_same_sex(
        self,
        husband_sex: Sex,
        wife_sex: Sex,
        person_factory: PersonFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        husband = person_factory.build(
            sex=husband_sex,
        )
        person_gateway.save(
            person=husband,
        )
        wife = person_factory.build(
            sex=wife_sex,
        )
        person_gateway.save(
            person=wife,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband.id,
            wife_id=wife.id,
            child_ids=[],
            status=MarriageStatus.MARRIAGE,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(DomainError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSONS_HAVE_SAME_SEX


class TestCreateMarriageShouldRaiseMarriageAlreadyExistsError:
    @pytest.mark.parametrize(
        argnames="marriage_status_to_use_in_command",
        argvalues=(
            MarriageStatus.MARRIAGE,
            MarriageStatus.HE_FILED_FOR_DIVORCE,
            MarriageStatus.SHE_FILED_FOR_DIVORCE,
        ),
    )
    @pytest.mark.parametrize(
        argnames="marriage_status",
        argvalues=(
            MarriageStatus.MARRIAGE,
            MarriageStatus.HE_FILED_FOR_DIVORCE,
            MarriageStatus.SHE_FILED_FOR_DIVORCE,
        ),
    )
    def when_marriage_already_exists(
        self,
        marriage_status_to_use_in_command: MarriageStatus,
        marriage_status: MarriageStatus,
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
            status=marriage_status,
        )
        marriage_gateway.save(
            marriage=marriage,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband.id,
            wife_id=wife.id,
            child_ids=[],
            status=marriage_status_to_use_in_command,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == MARRIAGE_ALREADY_EXISTS


@pytest.mark.parametrize(
    argnames="marriage_status_to_use_in_command",
    argvalues=(
        MarriageStatus.MARRIAGE,
        MarriageStatus.HE_FILED_FOR_DIVORCE,
        MarriageStatus.SHE_FILED_FOR_DIVORCE,
    ),
)
class TestCreateMarriageShouldRaisePersonIsMarriedError:
    @pytest.mark.parametrize(
        argnames="husband_marriage_status",
        argvalues=(
            MarriageStatus.MARRIAGE,
            MarriageStatus.HE_FILED_FOR_DIVORCE,
            MarriageStatus.SHE_FILED_FOR_DIVORCE,
        ),
    )
    def when_husband_is_married(
        self,
        husband_marriage_status: MarriageStatus,
        marriage_status_to_use_in_command: MarriageStatus,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        marriage_gateway: MarriageGateway,
        unit_of_work: UnitOfWork,
        identity_provider_with_valid_access_policy: IdentityProvider,
    ) -> None:
        wife = person_factory.build(
            sex=Sex.FEMALE,
        )
        person_gateway.save(
            person=wife,
        )
        marriage_husband = person_factory.build(
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=marriage_husband,
        )
        marriage_wife = person_factory.build(
            sex=Sex.FEMALE,
        )
        person_gateway.save(
            person=marriage_wife,
        )
        husband_marriage = marriage_factory.build(
            husband_id=marriage_husband.id,
            wife_id=marriage_wife.id,
            status=husband_marriage_status,
        )
        marriage_gateway.save(
            marriage=husband_marriage,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=marriage_husband.id,
            wife_id=wife.id,
            child_ids=[],
            status=marriage_status_to_use_in_command,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSON_IS_MARRIED
        assert error.value.extra["person_id"] == marriage_husband.id

    @pytest.mark.parametrize(
        argnames="wife_marriage_status",
        argvalues=(
            MarriageStatus.MARRIAGE,
            MarriageStatus.HE_FILED_FOR_DIVORCE,
            MarriageStatus.SHE_FILED_FOR_DIVORCE,
        ),
    )
    def when_wife_is_married(
        self,
        wife_marriage_status: MarriageStatus,
        marriage_status_to_use_in_command: MarriageStatus,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        person_gateway: PersonGateway,
        marriage_gateway: MarriageGateway,
        unit_of_work: UnitOfWork,
        identity_provider_with_valid_access_policy: IdentityProvider,
    ) -> None:
        husband = person_factory.build(
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=husband,
        )
        marriage_husband = person_factory.build(
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=marriage_husband,
        )
        marriage_wife = person_factory.build(
            sex=Sex.FEMALE,
        )
        person_gateway.save(
            person=marriage_wife,
        )
        husband_marriage = marriage_factory.build(
            husband_id=marriage_husband.id,
            wife_id=marriage_wife.id,
            status=wife_marriage_status,
        )
        marriage_gateway.save(
            marriage=husband_marriage,
        )
        unit_of_work.commit()

        create_marriage_command = CreateMarriageCommand(
            husband_id=husband.id,
            wife_id=marriage_wife.id,
            child_ids=[],
            status=marriage_status_to_use_in_command,
            start_date=None,
            end_date=None,
        )
        create_marriage_handler = CreateMarriageHandler(
            access_concern=AccessConcern(),
            create_marriage=CreateMarriage(),
            access_policy_gateway=access_policy_gateway,
            marriage_gateway=marriage_gateway,
            person_gateway=person_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_marriage_handler.execute(
                command=create_marriage_command,
            )

        assert error.value.message == PERSON_IS_MARRIED
        assert error.value.extra["person_id"] == marriage_wife.id
