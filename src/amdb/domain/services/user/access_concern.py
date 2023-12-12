from amdb.domain.services.base import Service
from amdb.domain.entities.user.access_policy import AccessPolicy


class AccessConcern(Service):
    def authorize(
        self,
        *,
        required_access_policy: AccessPolicy,
        current_access_policy: AccessPolicy,
    ) -> bool:
        return (
            required_access_policy.is_active == current_access_policy.is_active
            and required_access_policy.is_verified == current_access_policy.is_verified
        )
