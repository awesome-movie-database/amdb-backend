from unittest.mock import Mock
from typing import Annotated
from uuid import uuid4

import pytest
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user.user import UserId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.infrastructure.in_memory.access_policy_gateway import InMemoryAccessPolicyGateway
from amdb.infrastructure.database.gateways.user.user import SQLAlchemyUserGateway
from amdb.infrastructure.database.gateways.user.profile import SQLAlchemyProfileGateway
from amdb.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork
from amdb.infrastructure.database.mappers.user.user import UserMapper
from amdb.infrastructure.database.mappers.user.profile import ProfileMapper


SYSTEM_USER_ID = UserId(uuid4())


@pytest.fixture(scope="session")
def system_user_id() -> UserId:
    return SYSTEM_USER_ID


@pytest.fixture(scope="session")
def access_policy_gateway() -> InMemoryAccessPolicyGateway:
    return InMemoryAccessPolicyGateway(
        system_user_id=SYSTEM_USER_ID,
    )


@pytest.fixture(scope="session")
def user_mapper() -> UserMapper:
    return UserMapper()


@pytest.fixture(scope="session")
def profile_mapper() -> ProfileMapper:
    return ProfileMapper()


@pytest.fixture
def user_gateway(
    sqlalchemy_session: Session,
    user_mapper: UserMapper,
) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUserGateway(
        session=sqlalchemy_session,
        mapper=user_mapper,
    )


@pytest.fixture
def profile_gateway(
    sqlalchemy_session: Session,
    profile_mapper: ProfileMapper,
) -> SQLAlchemyProfileGateway:
    return SQLAlchemyProfileGateway(
        session=sqlalchemy_session,
        mapper=profile_mapper,
    )


@pytest.fixture
def unit_of_work(sqlalchemy_session: Session) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(
        session=sqlalchemy_session,
    )


@pytest.fixture
def identity_provider() -> Annotated[IdentityProvider, Mock]:
    identity_provider_mock = Mock()
    identity_provider_mock.get_access_policy = Mock()
    return identity_provider_mock
