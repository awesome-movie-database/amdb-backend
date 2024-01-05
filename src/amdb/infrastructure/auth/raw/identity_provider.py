from amdb.domain.entities.user import UserId
from amdb.application.common.interfaces.identity_provider import IdentityProvider


class RawIdentityProvider(IdentityProvider):
    def __init__(self, user_id: UserId, permissions: int) -> None:
        self._user_id = user_id
        self._permissions = permissions

    def get_user_id(self) -> UserId:
        return self._user_id

    def get_permissions(self) -> int:
        return self._permissions
