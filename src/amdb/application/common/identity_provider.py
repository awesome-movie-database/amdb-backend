from typing import Protocol

from amdb.domain.entities.user import UserId


class IdentityProvider(Protocol):
    def get_user_id(self) -> UserId:
        raise NotImplementedError

    def get_permissions(self) -> int:
        raise NotImplementedError
