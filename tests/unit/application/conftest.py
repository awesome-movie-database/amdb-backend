import pytest
from unittest.mock import Mock
from typing import Annotated

from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.gateways.user.profile import ProfileGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork


@pytest.fixture
def access_policy_gateway() -> Annotated[AccessPolicyGateway, Mock]:
    access_policy_gateway_mock = Mock()
    access_policy_gateway_mock.for_update_user = Mock()
    return access_policy_gateway_mock


@pytest.fixture
def user_gateway() -> Annotated[UserGateway, Mock]:
    user_gateway_mock = Mock()
    user_gateway_mock.check_with_name = Mock()
    user_gateway_mock.with_id = Mock()
    user_gateway_mock.save = Mock()
    user_gateway_mock.update = Mock()
    return user_gateway_mock


@pytest.fixture
def profile_gateway() -> Annotated[ProfileGateway, Mock]:
    profile_gateway_mock = Mock()
    profile_gateway_mock.with_user_id = Mock()
    profile_gateway_mock.save = Mock()
    profile_gateway_mock.update = Mock()
    return profile_gateway_mock


@pytest.fixture
def identity_provider() -> Annotated[IdentityProvider, Mock]:
    identity_provider_mock = Mock()
    identity_provider_mock.get_access_policy = Mock()
    return identity_provider_mock


@pytest.fixture
def unit_of_work() -> Annotated[UnitOfWork, Mock]:
    unit_of_work_mock = Mock()
    unit_of_work_mock.commit = Mock()
    unit_of_work_mock.rollback = Mock()
    return unit_of_work_mock
