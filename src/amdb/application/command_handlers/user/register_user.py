from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.user.user import UserId
from amdb.domain.services.user.create_user import CreateUser
from amdb.domain.services.user.create_profile import CreateProfile
from amdb.application.commands.user.register_user import RegisterUserCommand
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.gateways.user.profile import ProfileGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError


class RegisterUserHandler:
    def __init__(
        self,
        *,
        create_user: CreateUser,
        create_profile: CreateProfile,
        user_gateway: UserGateway,
        profile_gateway: ProfileGateway,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._create_user = create_user
        self._create_profile = create_profile
        self._user_gateway = user_gateway
        self._profile_gateway = profile_gateway
        self._unit_of_work = unit_of_work

    def execute(self, command: RegisterUserCommand) -> UserId:
        user = self._user_gateway.with_name(
            user_name=command.name,
        )
        if user:
            raise ApplicationError(USER_NAME_ALREADY_EXISTS)

        user = self._create_user(
            id=UserId(uuid4()),
            name=command.name,
            password=command.password,
            timestamp=datetime.now(timezone.utc),
            email=command.email,
            sex=command.sex,
            birth_date=command.birth_date,
            location=command.location,
        )
        self._user_gateway.save(
            user=user,
        )

        profile = self._create_profile(
            user=user,
        )
        self._profile_gateway.save(
            profile=profile,
        )

        self._unit_of_work.commit()

        return user.id
