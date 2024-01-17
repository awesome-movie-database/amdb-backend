from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId
from amdb.domain.services.create_user import CreateUser
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.interfaces.password_manager import PasswordManager
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.register_user import RegisterUserCommand


class RegisterUserHandler:
    def __init__(
        self,
        *,
        create_user: CreateUser,
        user_gateway: UserGateway,
        unit_of_work: UnitOfWork,
        password_manager: PasswordManager,
    ) -> None:
        self._create_user = create_user
        self._user_gateway = user_gateway
        self._unit_of_work = unit_of_work
        self._password_manager = password_manager

    def execute(self, command: RegisterUserCommand) -> UserId:
        user = self._user_gateway.with_name(command.name)
        if user:
            raise ApplicationError(USER_NAME_ALREADY_EXISTS)

        new_user = self._create_user(
            id=UserId(uuid7()),
            name=command.name,
        )
        self._user_gateway.save(new_user)

        self._password_manager.set(
            user_id=new_user.id,
            password=command.password,
        )

        self._unit_of_work.commit()

        return new_user.id
