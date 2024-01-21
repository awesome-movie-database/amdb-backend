from typing import cast

from amdb.domain.entities.user import UserId
from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.permissions_gateway import PermissionsGateway
from amdb.application.common.interfaces.password_manager import PasswordManager
from amdb.application.common.constants.exceptions import (
    LOGIN_ACCESS_DENIED,
    USER_DOES_NOT_EXIST,
    INCORRECT_PASSWORD,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.login import LoginQuery


class LoginHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        password_manager: PasswordManager,
    ) -> None:
        self._access_concern = access_concern
        self._user_gateway = user_gateway
        self._permissions_gateway = permissions_gateway
        self._password_manager = password_manager

    def execute(self, query: LoginQuery) -> UserId:
        user = self._user_gateway.with_name(query.name)
        if not user:
            raise ApplicationError(USER_DOES_NOT_EXIST)

        password_is_correct = self._password_manager.verify(
            user_id=user.id,
            password=query.password,
        )
        if not password_is_correct:
            raise ApplicationError(INCORRECT_PASSWORD)

        user_permissions = self._permissions_gateway.with_user_id(user.id)
        user_permissions = cast(int, user_permissions)

        required_permissions = self._permissions_gateway.for_login()
        access = self._access_concern.authorize(
            current_permissions=user_permissions,
            required_permissions=required_permissions,
        )
        if not access:
            raise ApplicationError(LOGIN_ACCESS_DENIED)

        return user.id
