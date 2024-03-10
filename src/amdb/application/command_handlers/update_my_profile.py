from typing import cast

from amdb.domain.entities.user import User
from amdb.domain.services.update_profile import UpdateProfile
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.update_my_profile import UpdateMyProfileCommand


class UpdateMyProfileHandler:
    def __init__(
        self,
        *,
        update_profile: UpdateProfile,
        user_gateway: UserGateway,
        unit_of_work: UnitOfWork,
        identity_provider: IdentityProvider,
    ) -> None:
        self._update_profile = update_profile
        self._user_gateway = user_gateway
        self._unit_of_work = unit_of_work
        self._identity_provider = identity_provider

    def execute(self, command: UpdateMyProfileCommand) -> None:
        current_user_id = self._identity_provider.user_id()

        user = self._user_gateway.with_id(current_user_id)
        user = cast(User, user)

        self._update_profile(
            user=user,
            email=command.email,
        )
        self._user_gateway.update(user)

        self._unit_of_work.commit()
