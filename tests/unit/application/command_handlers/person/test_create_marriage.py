from unittest.mock import Mock

import pytest

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import Marriage
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_MARRIAGE_ACCESS_DENIED,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_marriage import CreateMarriageCommand
from amdb.application.command_handlers.person.create_marriage import CreateMarriageHandler


@pytest.mark.usefixtures("clear_database")
def test_create_marriage(
    system_user_id: UserId,
    marriage: Marriage,
    person: Person,
    other_person: Person,
    access_concern: AccessConcern,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    create_marriage: CreateMarriage = Mock(
        return_value=marriage,
    )
    current_access_policy = AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    person_gateway.save(
        person=person,
    )
    person_gateway.save(
        person=other_person,
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
        access_concern=access_concern,
        create_marriage=create_marriage,
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    create_marriage_handler.execute(
        command=create_marriage_command,
    )


@pytest.mark.usefixtures("clear_database")
def test_create_marriage_should_raise_error_when_access_is_denied(
    user: User,
    marriage: Marriage,
    person: Person,
    other_person: Person,
    access_concern: AccessConcern,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    create_marriage: CreateMarriage = Mock(
        return_value=marriage,
    )
    current_access_policy = AccessPolicy(
        id=user.id,
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    person_gateway.save(
        person=person,
    )
    person_gateway.save(
        person=other_person,
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
        access_concern=access_concern,
        create_marriage=create_marriage,
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


@pytest.mark.usefixtures("clear_database")
def test_create_marriage(
    system_user_id: UserId,
    marriage: Marriage,
    person: Person,
    other_person: Person,
    access_concern: AccessConcern,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    create_marriage: CreateMarriage = Mock(
        return_value=marriage,
    )
    current_access_policy = AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )
    person_gateway.save(
        person=person,
    )
    person_gateway.save(
        person=other_person,
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
        access_concern=access_concern,
        create_marriage=create_marriage,
        access_policy_gateway=access_policy_gateway,
        marriage_gateway=marriage_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    create_marriage_handler.execute(
        command=create_marriage_command,
    )
