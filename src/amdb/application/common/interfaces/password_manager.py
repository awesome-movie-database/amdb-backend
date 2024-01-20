from typing import Protocol

from amdb.domain.entities.user import UserId


class PasswordManager(Protocol):
    def set(self, user_id: UserId, password: str) -> None:
        raise NotImplementedError

    def verify(self, user_id: UserId, password: str) -> bool:
        raise NotImplementedError
