from unittest.mock import Mock
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import MarriageStatus, Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_PERSON_INVALID_COMMAND,
    CREATE_MARRIAGE_ACCESS_DENIED,
    PERSON_DOES_NOT_EXIST,
    PERSONS_DO_NOT_EXIST,
    MARRIAGE_ALREADY_EXISTS,
    PERSONS_HAVE_SAME_SEX,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_marriage import CreateMarriageCommand
from amdb.application.command_handlers.person.create_marriage import CreateMarriageHandler


HUSBAND_ID = PersonId(uuid4())
WIFE_ID = PersonId(uuid4())


@pytest.fixture(scope="module")
def valid_access_policy(
    system_user_id: UserId,
) -> AccessPolicy:
    return AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )


@pytest.mark.usefixtures("clear_database")
def test_create_marriage(
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        sex=Sex.MALE,
    )
    wife = person_factory.build(
        sex=Sex.FEMALE,
    )
    child = person_factory.build()
    marriage_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Marriage,
    )
    marriage = marriage_factory.build(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[child.id],
    )
    create_marriage: CreateMarriage = Mock(
        return_value=marriage,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    person_gateway.save(
        person=wife,
    )
    person_gateway.save(
        person=child,
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
        create_marriage=create_marriage,
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    marriage_id = create_marriage_handler.execute(
        command=create_marriage_command,
    )

    assert marriage_id == marriage.id


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_access_is_denied(
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        sex=Sex.MALE,
    )
    wife = person_factory.build(
        sex=Sex.FEMALE,
    )
    child = person_factory.build()
    invalid_access_policy = AccessPolicy(
        id=UserId(uuid4()),
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=invalid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    person_gateway.save(
        person=wife,
    )
    person_gateway.save(
        person=child,
    )
    unit_of_work.commit()
    create_marriage_command = CreateMarriageCommand(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[child.id],
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == CREATE_MARRIAGE_ACCESS_DENIED


@pytest.mark.parametrize(
    argnames=("child_id"),
    argvalues=(HUSBAND_ID, WIFE_ID),
)
@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_command_is_invalid(
    child_id: PersonId,
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        id=HUSBAND_ID,
        sex=Sex.MALE,
    )
    wife = person_factory.build(
        id=WIFE_ID,
        sex=Sex.FEMALE,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    person_gateway.save(
        person=wife,
    )
    unit_of_work.commit()
    create_marriage_command = CreateMarriageCommand(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[child_id],
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == CREATE_PERSON_INVALID_COMMAND


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_children_do_not_exist(
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        id=HUSBAND_ID,
        sex=Sex.MALE,
    )
    wife = person_factory.build(
        id=WIFE_ID,
        sex=Sex.FEMALE,
    )
    child_ids = [PersonId(uuid4())]
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    person_gateway.save(
        person=wife,
    )
    unit_of_work.commit()
    create_marriage_command = CreateMarriageCommand(
        husband_id=husband.id,
        wife_id=wife.id,
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == PERSONS_DO_NOT_EXIST
    assert error.value.extra["person_ids"] == child_ids


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_husband_does_not_exist(
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    wife = person_factory.build(
        sex=Sex.FEMALE,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=wife,
    )
    unit_of_work.commit()
    create_marriage_command = CreateMarriageCommand(
        husband_id=HUSBAND_ID,
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == PERSON_DOES_NOT_EXIST
    assert error.value.extra["person_id"] == HUSBAND_ID


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_wife_does_not_exist(
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        sex=Sex.MALE,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    unit_of_work.commit()
    create_marriage_command = CreateMarriageCommand(
        husband_id=husband.id,
        wife_id=WIFE_ID,
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == PERSON_DOES_NOT_EXIST
    assert error.value.extra["person_id"] == WIFE_ID


@pytest.mark.parametrize(
    argnames=("husband_sex", "wife_sex"),
    argvalues=((Sex.MALE, Sex.MALE), (Sex.FEMALE, Sex.FEMALE)),
)
@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_husband_or_wife_have_same_sex(
    valid_access_policy: AccessPolicy,
    husband_sex: Sex,
    wife_sex: Sex,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        sex=husband_sex,
    )
    wife = person_factory.build(
        sex=wife_sex,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == PERSONS_HAVE_SAME_SEX


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_marriage_already_exists(
    valid_access_policy: AccessPolicy,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    person_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Person,
    )
    husband = person_factory.build(
        sex=Sex.MALE,
    )
    wife = person_factory.build(
        sex=Sex.FEMALE,
    )
    marriage_factory = DataclassFactory.create_factory(  # type: ignore[var-annotated]
        model=Marriage,
    )
    marriage = marriage_factory.build(
        husband_id=husband.id,
        wife_id=wife.id,
        child_ids=[],
        status=MarriageStatus.MARRIAGE,
    )
    identity_provider.get_access_policy = Mock(
        return_value=valid_access_policy,
    )
    person_gateway.save(
        person=husband,
    )
    person_gateway.save(
        person=wife,
    )
    marriage_gateway.save(
        marriage=marriage,
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
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        create_marriage_handler.execute(
            command=create_marriage_command,
        )

    assert error.value.messsage == MARRIAGE_ALREADY_EXISTS
