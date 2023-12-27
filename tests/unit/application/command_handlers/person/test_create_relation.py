from unittest.mock import Mock
from typing import Type
from uuid import uuid4

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.access_policy import AccessPolicy
from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import Marriage
from amdb.domain.entities.person.relation import RelationType, Relation
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.person.create_relation import CreateRelation
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.person.marriage import MarriageGateway
from amdb.application.common.interfaces.gateways.person.person import PersonGateway
from amdb.application.common.interfaces.gateways.person.relation import RelationGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    CREATE_RELATION_INVALID_COMMAND,
    CREATE_RELATION_ACCESS_DENIED,
    RELATION_ALREADY_EXISTS,
    PERSON_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.person.create_relation import CreateRelationCommand
from amdb.application.command_handlers.person.create_relation import CreateRelationHandler


PersonFactory = Type[DataclassFactory[Person]]
MarriageFactory = Type[DataclassFactory[Marriage]]
RelationFactory = Type[DataclassFactory[Relation]]

PERSON_ID = PersonId(uuid4())
RELATIVE_ID = PersonId(uuid4())


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


def test_create_relation(
    person_factory: PersonFactory,
    access_policy_gateway: AccessPolicyGateway,
    marriage_gateway: MarriageGateway,
    person_gateway: PersonGateway,
    relation_gateway: RelationGateway,
    identity_provider_with_valid_access_policy: IdentityProvider,
    unit_of_work: UnitOfWork,
) -> None:
    grandfather = person_factory.build(
        name="John Doe",
        sex=Sex.MALE,
        birth_date=Date(year=1945, month=12, day=19),
    )
    person_gateway.save(
        person=grandfather,
    )
    grandson = person_factory.build(
        name="Johny Doe",
        sex=Sex.MALE,
        birth_date=Date(year=2001, month=7, day=15),
    )
    person_gateway.save(
        person=grandson,
    )
    unit_of_work.commit()

    create_relation_command = CreateRelationCommand(
        person_id=grandfather.id,
        relative_id=grandson.id,
        type=RelationType.GRANDCHILD,
    )
    create_relation_handler = CreateRelationHandler(
        access_concern=AccessConcern(),
        create_relation=CreateRelation(),
        access_policy_gateway=access_policy_gateway,
        relation_gateway=relation_gateway,
        person_gateway=person_gateway,
        marriage_gateway=marriage_gateway,
        identity_provider=identity_provider_with_valid_access_policy,
        unit_of_work=unit_of_work,
    )

    create_relation_handler.execute(
        command=create_relation_command,
    )


class TestCreateRelationShouldRaiseCreateRelationAccessDeniedError:
    def when_access_is_denied(
        self,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        identity_provider_with_invalid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        create_relation_command = CreateRelationCommand(
            person_id=PersonId(uuid4()),
            relative_id=PersonId(uuid4()),
            type=RelationType.AUNCLE,
        )
        create_relation_handler = CreateRelationHandler(
            access_concern=AccessConcern(),
            create_relation=CreateRelation(),
            access_policy_gateway=access_policy_gateway,
            relation_gateway=relation_gateway,
            person_gateway=person_gateway,
            marriage_gateway=marriage_gateway,
            identity_provider=identity_provider_with_invalid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_relation_handler.execute(
                command=create_relation_command,
            )

        assert error.value.message == CREATE_RELATION_ACCESS_DENIED


class TestCreateRelationShouldRaiseRelationAlreadyExistsError:
    def when_relation_already_exists(
        self,
        person_factory: PersonFactory,
        relation_factory: RelationFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        grandfather = person_factory.build(
            name="John Doe",
            sex=Sex.MALE,
            birth_date=Date(year=1945, month=12, day=19),
        )
        person_gateway.save(
            person=grandfather,
        )
        grandson = person_factory.build(
            name="Johny Doe",
            sex=Sex.MALE,
            birth_date=Date(year=2001, month=7, day=15),
        )
        person_gateway.save(
            person=grandson,
        )
        relation = relation_factory.build(
            person_id=grandfather.id,
            relative_id=grandson.id,
            type=RelationType.GRANDCHILD,
        )
        relation_gateway.save(
            relation=relation,
        )
        unit_of_work.commit()

        create_relation_command = CreateRelationCommand(
            person_id=relation.person_id,
            relative_id=relation.relative_id,
            type=relation.type,
        )
        create_relation_handler = CreateRelationHandler(
            access_concern=AccessConcern(),
            create_relation=CreateRelation(),
            access_policy_gateway=access_policy_gateway,
            relation_gateway=relation_gateway,
            person_gateway=person_gateway,
            marriage_gateway=marriage_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_relation_handler.execute(
                command=create_relation_command,
            )

        assert error.value.message == RELATION_ALREADY_EXISTS


class TestCreateRelationShouldRaisePersonDoesNotExistError:
    def when_person_does_not_exist(
        self,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        nonexistent_person_id = PersonId(uuid4())

        relative = person_factory.build()
        person_gateway.save(
            person=relative,
        )
        unit_of_work.commit()

        create_relation_command = CreateRelationCommand(
            person_id=nonexistent_person_id,
            relative_id=relative.id,
            type=RelationType.SIBLING,
        )
        create_relation_handler = CreateRelationHandler(
            access_concern=AccessConcern(),
            create_relation=CreateRelation(),
            access_policy_gateway=access_policy_gateway,
            relation_gateway=relation_gateway,
            person_gateway=person_gateway,
            marriage_gateway=marriage_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_relation_handler.execute(
                command=create_relation_command,
            )

        assert error.value.message == PERSON_DOES_NOT_EXIST
        assert error.value.extra["person_id"] == nonexistent_person_id

    def when_relative_does_not_exist(
        self,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        nonexistent_relative_id = PersonId(uuid4())

        person = person_factory.build()
        person_gateway.save(
            person=person,
        )
        unit_of_work.commit()

        create_relation_command = CreateRelationCommand(
            person_id=person.id,
            relative_id=nonexistent_relative_id,
            type=RelationType.SIBLING,
        )
        create_relation_handler = CreateRelationHandler(
            access_concern=AccessConcern(),
            create_relation=CreateRelation(),
            access_policy_gateway=access_policy_gateway,
            relation_gateway=relation_gateway,
            person_gateway=person_gateway,
            marriage_gateway=marriage_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_relation_handler.execute(
                command=create_relation_command,
            )

        assert error.value.message == PERSON_DOES_NOT_EXIST
        assert error.value.extra["person_id"] == nonexistent_relative_id


class TestCreateRelationShouldRaiseCreateRelationInvalidCommandError:
    @pytest.mark.parametrize(
        argnames=(
            "person_id",
            "relative_id",
        ),
        argvalues=(
            (
                PERSON_ID,
                RELATIVE_ID,
            ),
            (RELATIVE_ID, PERSON_ID),
        ),
    )
    def when_person_and_relative_are_married_or_were_married(
        self,
        person_id: PersonId,
        relative_id: PersonId,
        person_factory: PersonFactory,
        marriage_factory: MarriageFactory,
        access_policy_gateway: AccessPolicyGateway,
        marriage_gateway: MarriageGateway,
        person_gateway: PersonGateway,
        relation_gateway: RelationGateway,
        identity_provider_with_valid_access_policy: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        husband = person_factory.build(
            id=person_id,
            sex=Sex.MALE,
        )
        person_gateway.save(
            person=husband,
        )
        wife = person_factory.build(
            id=relative_id,
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

        create_relation_command = CreateRelationCommand(
            person_id=person_id,
            relative_id=relative_id,
            type=RelationType.SIBLING,
        )
        create_relation_handler = CreateRelationHandler(
            access_concern=AccessConcern(),
            create_relation=CreateRelation(),
            access_policy_gateway=access_policy_gateway,
            relation_gateway=relation_gateway,
            person_gateway=person_gateway,
            marriage_gateway=marriage_gateway,
            identity_provider=identity_provider_with_valid_access_policy,
            unit_of_work=unit_of_work,
        )

        with pytest.raises(ApplicationError) as error:
            create_relation_handler.execute(
                command=create_relation_command,
            )

        assert error.value.message == CREATE_RELATION_INVALID_COMMAND
