from typing import Protocol

from amdb.domain.entities.user.access_policy import AccessPolicy


class AccessPolicyGateway(Protocol):
    def for_update_user(self) -> AccessPolicy:
        raise NotImplementedError
