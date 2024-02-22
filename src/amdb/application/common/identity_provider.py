from typing import Protocol, Optional

from amdb.domain.entities.user import UserId


class IdentityProvider(Protocol):
    def user_id(self) -> UserId:
        raise NotImplementedError

    def user_id_or_none(self) -> Optional[UserId]:
        raise NotImplementedError

    def permissions(self) -> int:
        raise NotImplementedError
