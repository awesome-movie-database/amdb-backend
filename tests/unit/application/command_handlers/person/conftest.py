from typing import Type

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.person.person import Person
from amdb.domain.entities.person.marriage import Marriage


PersonFactory = Type[DataclassFactory[Person]]
MarriageFactory = Type[DataclassFactory[Marriage]]


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
