from amdb.domain.entities.user.user import UserId
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway
from amdb.domain.entities.user.access_policy import RequiredAccessPolicy


class InMemoryAccessPolicyGateway(AccessPolicyGateway):
    def __init__(
        self,
        *,
        system_user_id: UserId,
    ) -> None:
        self._system_user_id = system_user_id

    def for_update_user(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            is_active=True,
            is_verified=None,
            id=None,
        )

    def for_verify_user(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=self._system_user_id,
            is_active=None,
            is_verified=None,
        )
