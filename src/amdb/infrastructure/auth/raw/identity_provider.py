from uuid import UUID

from amdb.domain.entities.user import UserId
from amdb.application.common.interfaces.identity_provider import IdentityProvider


class RawIdentityProvider(IdentityProvider):
    def get_user_id(self) -> UserId:
        return UserId(UUID("00000000-0000-0000-0000-000000000000"))

    def get_permissions(self) -> int:
        return 2
