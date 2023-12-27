from typing import Type

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import Marriage
from amdb.domain.entities.person.relation import Relation


PersonFactory = Type[DataclassFactory[Person]]
MarriageFactory = Type[DataclassFactory[Marriage]]
RelationGateway = Type[DataclassFactory[Relation]]


@pytest.fixture(scope="package")
def person_factory() -> PersonFactory:
    return DataclassFactory.create_factory(
        model=Person,
    )


@pytest.fixture(scope="package")
def marriage_factory() -> MarriageFactory:
    return DataclassFactory.create_factory(
        model=Marriage,
        child_ids=[],
        start_date=None,
        end_date=None,
    )


@pytest.fixture(scope="package")
def relation_factory() -> Relation:
    return DataclassFactory.create_factory(
        model=Relation,
    )
