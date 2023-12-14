from typing import Protocol

from amdb.domain.entities.user.access_policy import AccessPolicyWithIdentity


class IdentityProvider(Protocol):
    def get_access_policy(self) -> AccessPolicyWithIdentity:
        raise NotImplementedError
