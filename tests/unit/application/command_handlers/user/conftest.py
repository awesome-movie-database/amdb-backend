from typing import Type

import pytest
from polyfactory.factories import DataclassFactory

from amdb.domain.entities.user.user import User


UserFactory = Type[DataclassFactory[User]]


@pytest.fixture(scope="package")
def user_factory() -> UserFactory:
    return DataclassFactory.create_factory(
        model=User,
        is_active=True,
        is_verified=False,
        updated_at=None,
    )
