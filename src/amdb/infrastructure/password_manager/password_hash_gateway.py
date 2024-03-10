from typing import Protocol, Optional

from amdb.domain.entities.user import UserId
from amdb.infrastructure.password_manager.password_hash import PasswordHash


class PasswordHashGateway(Protocol):
    def with_user_id(self, user_id: UserId) -> Optional[PasswordHash]:
        raise NotImplementedError

    def save(self, password_hash: PasswordHash) -> None:
        raise NotImplementedError
