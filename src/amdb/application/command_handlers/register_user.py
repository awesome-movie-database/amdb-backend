from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId
from amdb.domain.services.create_user import CreateUser
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.permissions import (
    PermissionsGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.password_manager import PasswordManager
from amdb.application.common.constants.exceptions import (
    USER_NAME_ALREADY_EXISTS,
    USER_EMAIL_ALREADY_EXISTS,
    USER_TELEGRAM_ALREADY_EXISTS,
)
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.register_user import RegisterUserCommand


class RegisterUserHandler:
    def __init__(
        self,
        *,
        create_user: CreateUser,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        unit_of_work: UnitOfWork,
        password_manager: PasswordManager,
    ) -> None:
        self._create_user = create_user
        self._user_gateway = user_gateway
        self._permissions_gateway = permissions_gateway
        self._unit_of_work = unit_of_work
        self._password_manager = password_manager

    def execute(self, command: RegisterUserCommand) -> UserId:
        user = self._user_gateway.with_name(command.name)
        if user:
            raise ApplicationError(USER_NAME_ALREADY_EXISTS)

        if command.email:
            self._ensure_email_is_not_taken(command.email)
        if command.telegram:
            self._ensure_telegram_is_not_taken(command.telegram)

        new_user = self._create_user(
            id=UserId(uuid7()),
            name=command.name,
            email=command.email,
            telegram=command.telegram,
        )
        self._user_gateway.save(new_user)

        self._permissions_gateway.set(
            user_id=new_user.id,
            permissions=self._permissions_gateway.for_new_user(),
        )
        self._password_manager.set(
            user_id=new_user.id,
            password=command.password,
        )

        self._unit_of_work.commit()

        return new_user.id

    def _ensure_email_is_not_taken(self, email: str) -> None:
        user = self._user_gateway.with_email(email)
        if user:
            raise ApplicationError(USER_EMAIL_ALREADY_EXISTS)

    def _ensure_telegram_is_not_taken(self, telegram: str) -> None:
        user = self._user_gateway.with_telegram(telegram)
        if user:
            raise ApplicationError(USER_TELEGRAM_ALREADY_EXISTS)
