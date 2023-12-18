from unittest.mock import Mock

import pytest

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.entities.person.person import Person
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


NEW_PERSON_NAME = "John Doe jr"


@pytest.mark.usefixtures("clear_database")
def test_update_person(
    system_user_id: UserId,
    person: Person,
    access_concern: AccessConcern,
    update_person: UpdatePerson,
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
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
    unit_of_work.commit()

    update_person_command = UpdatePersonCommand(
        person_id=person.id,
        name=NEW_PERSON_NAME,
    )
    update_person_handler = UpdatePersonHandler(
        access_concern=access_concern,
        update_person=update_person,
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    update_person_handler.execute(
        command=update_person_command,
    )


@pytest.mark.usefixtures("clear_database")
def test_update_person_should_raise_error_when_access_is_denied(
    user: User,
    person: Person,
    access_concern: AccessConcern,
    update_person: UpdatePerson,
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
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
    unit_of_work.commit()

    update_person_command = UpdatePersonCommand(
        person_id=person.id,
        name=NEW_PERSON_NAME,
    )
    update_person_handler = UpdatePersonHandler(
        access_concern=access_concern,
        update_person=update_person,
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        update_person_handler.execute(
            command=update_person_command,
        )
    assert error.value.messsage == UPDATE_PERSON_ACCESS_DENIED


@pytest.mark.usefixtures("clear_database")
def test_update_person_should_raise_error_when_person_does_not_exist(
    system_user_id: UserId,
    person: Person,
    access_concern: AccessConcern,
    update_person: UpdatePerson,
    access_policy_gateway: AccessPolicyGateway,
    person_gateway: PersonGateway,
    identity_provider: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    current_access_policy = AccessPolicy(
        id=system_user_id,
        is_active=True,
        is_verified=True,
    )
    identity_provider.get_access_policy = Mock(
        return_value=current_access_policy,
    )

    update_person_command = UpdatePersonCommand(
        person_id=person.id,
        name=NEW_PERSON_NAME,
    )
    update_person_handler = UpdatePersonHandler(
        access_concern=access_concern,
        update_person=update_person,
        access_policy_gateway=access_policy_gateway,
        person_gateway=person_gateway,
        identity_provider=identity_provider,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        update_person_handler.execute(
            command=update_person_command,
        )
    assert error.value.messsage == PERSON_DOES_NOT_EXIST
