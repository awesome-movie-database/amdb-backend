from typing import Optional

from amdb.domain.entities.user import UserId


class RawIdentityProvider:
    def __init__(self, user_id: UserId, permissions: int) -> None:
        self._user_id = user_id
        self._permissions = permissions

    def user_id(self) -> UserId:
        return self._user_id

    def user_id_or_none(self) -> Optional[UserId]:
        return self._user_id

    def permissions(self) -> int:
        return self._permissions
