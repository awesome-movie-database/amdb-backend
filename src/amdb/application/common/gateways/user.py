from typing import Optional, Protocol

from amdb.domain.entities.user import UserId, User


class UserGateway(Protocol):
    def with_id(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError

    def with_name(self, user_name: str) -> Optional[User]:
        raise NotImplementedError

    def with_email(self, user_email: str) -> Optional[User]:
        raise NotImplementedError

    def with_telegram(self, user_telegram: str) -> Optional[User]:
        raise NotImplementedError

    def save(self, user: User) -> None:
        raise NotImplementedError

    def update(self, user: User) -> None:
        raise NotImplementedError
