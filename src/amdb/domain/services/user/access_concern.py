from amdb.domain.entities.user.user import UserId

from amdb.domain.services.base import Service
from amdb.domain.entities.user.access_policy import AccessPolicyWithIdentity, RequiredAccessPolicy


class AccessConcern(Service):
    def __init__(
        self,
        *,
        system_user_id: UserId,
    ) -> None:
        self._system_user_id = system_user_id

    def authorize(
        self,
        *,
        required_access_policy: RequiredAccessPolicy,
        current_access_policy: AccessPolicyWithIdentity,
    ) -> bool:
        if (
            required_access_policy.id is not None
            and required_access_policy.id != current_access_policy.id
        ):
            return False

        return (
            required_access_policy.id == self._system_user_id
            or required_access_policy.is_active == current_access_policy.is_active
            and required_access_policy.is_verified == current_access_policy.is_verified
        )
