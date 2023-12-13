from datetime import datetime, timezone

from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.update_user import UpdateUser
from amdb.application.commands.user.update_user import UpdateUserCommand
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import (
    UPDATE_USER_ACCESS_DENIED,
    USER_DOES_NOT_EXIST,
)
from amdb.application.common.exception import ApplicationError


class UpdateUserHandler:
    def __init__(
        self,
        *,
        access_concern: AccessConcern,
        update_user: UpdateUser,
        access_policy_gateway: AccessPolicyGateway,
        user_gateway: UserGateway,
        identity_provider: IdentityProvider,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._access_concern = access_concern
        self._update_user = update_user
        self._access_policy_gateway = access_policy_gateway
        self._user_gateway = user_gateway
        self._identity_provider = identity_provider
        self._unit_of_work = unit_of_work

    def execute(self, command: UpdateUserCommand) -> None:
        current_access_policy = self._identity_provider.get_access_policy()
        required_access_policy = self._access_policy_gateway.for_update_user()
        access = self._access_concern.authorize(
            required_access_policy=required_access_policy,
            current_access_policy=current_access_policy,
        )
        if not access:
            raise ApplicationError(UPDATE_USER_ACCESS_DENIED)

        user = self._user_gateway.with_id(
            user_id=current_access_policy.id,  # type: ignore
        )
        if not user:
            raise ApplicationError(USER_DOES_NOT_EXIST)

        self._update_user(
            user=user,
            timestamp=datetime.now(timezone.utc),
            name=command.name,
            password=command.password,
            sex=command.sex,
            birth_date=command.birth_date,
            location=command.location,
        )
        self._user_gateway.update(
            user=user,
        )

        self._unit_of_work.commit()
