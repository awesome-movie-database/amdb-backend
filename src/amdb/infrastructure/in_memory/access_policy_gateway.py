from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.user.access_policy import no_matter, RequiredAccessPolicy
from amdb.application.common.interfaces.gateways.user.access_policy import AccessPolicyGateway


class InMemoryAccessPolicyGateway(AccessPolicyGateway):
    def __init__(
        self,
        *,
        system_user_id: UserId,
    ) -> None:
        self._system_user_id = system_user_id

    def for_update_user(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=no_matter,
            is_active=True,
            is_verified=no_matter,
        )

    def for_verify_user(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=self._system_user_id,
            is_active=no_matter,
            is_verified=no_matter,
        )

    def for_create_person(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=self._system_user_id,
            is_active=no_matter,
            is_verified=no_matter,
        )

    def for_update_person(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=self._system_user_id,
            is_active=no_matter,
            is_verified=no_matter,
        )

    def for_create_marriage(self) -> RequiredAccessPolicy:
        return RequiredAccessPolicy(
            id=self._system_user_id,
            is_active=no_matter,
            is_verified=no_matter,
        )
