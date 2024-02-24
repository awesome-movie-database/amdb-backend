import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.password_manager import PasswordManager
from amdb.application.queries.login import LoginQuery
from amdb.application.query_handlers.login import LoginHandler
from amdb.application.common.constants.exceptions import (
    LOGIN_ACCESS_DENIED,
    USER_DOES_NOT_EXIST,
    INCORRECT_PASSWORD,
)
from amdb.application.common.exception import ApplicationError


def test_login(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    password_manager: PasswordManager,
    unit_of_work: UnitOfWork,
):
    user_password = "secret"

    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    password_manager.set(
        user_id=user.id,
        password=user_password,
    )

    correct_permissions = permissions_gateway.for_login()
    permissions_gateway.set(
        user_id=user.id,
        permissions=correct_permissions,
    )

    unit_of_work.commit()

    login_query = LoginQuery(
        name=user.name,
        password=user_password,
    )
    login_handler = LoginHandler(
        access_concern=AccessConcern(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        password_manager=password_manager,
    )

    user_id = login_handler.execute(login_query)

    assert user_id == user.id


def test_login_should_raise_error_when_user_does_not_exist(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    password_manager: PasswordManager,
):
    login_query = LoginQuery(
        name="John Doe",
        password="secret",
    )
    login_handler = LoginHandler(
        access_concern=AccessConcern(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        login_handler.execute(login_query)

    assert error.value.message == USER_DOES_NOT_EXIST


def test_login_should_raise_error_when_password_is_incorrect(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    password_manager: PasswordManager,
    unit_of_work: UnitOfWork,
):
    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    password_manager.set(
        user_id=user.id,
        password="secret",
    )

    unit_of_work.commit()

    query = LoginQuery(
        name=user.name,
        password="invalid_password",
    )
    handler = LoginHandler(
        access_concern=AccessConcern(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(query)

    assert error.value.message == INCORRECT_PASSWORD


def test_login_should_raise_error_when_access_is_denied(
    user_gateway: UserGateway,
    permissions_gateway: PermissionsGateway,
    password_manager: PasswordManager,
    unit_of_work: UnitOfWork,
):
    user_password = "secret"

    user = User(
        id=UserId(uuid7()),
        name="John Doe",
    )
    user_gateway.save(user)

    password_manager.set(
        user_id=user.id,
        password=user_password,
    )

    incorrect_permissions = 0
    permissions_gateway.set(
        user_id=user.id,
        permissions=incorrect_permissions,
    )

    unit_of_work.commit()

    query = LoginQuery(
        name=user.name,
        password=user_password,
    )
    handler = LoginHandler(
        access_concern=AccessConcern(),
        user_gateway=user_gateway,
        permissions_gateway=permissions_gateway,
        password_manager=password_manager,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(query)

    assert error.value.message == LOGIN_ACCESS_DENIED
