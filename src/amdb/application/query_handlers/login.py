from amdb.domain.entities.user import UserId
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.password_manager import PasswordManager
from amdb.application.common.constants.exceptions import (
    USER_DOES_NOT_EXIST,
    INCORRECT_PASSWORD,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.queries.login import LoginQuery


class LoginHandler:
    def __init__(
        self,
        *,
        user_gateway: UserGateway,
        password_manager: PasswordManager,
    ) -> None:
        self._user_gateway = user_gateway
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

        return user.id
