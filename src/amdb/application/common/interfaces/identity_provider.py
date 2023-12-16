from typing import Protocol

from amdb.domain.entities.user.access_policy import AccessPolicy


class IdentityProvider(Protocol):
    def get_access_policy(self) -> AccessPolicy:
        raise NotImplementedError
