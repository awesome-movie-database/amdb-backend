from typing import Optional, Protocol

from amdb.domain.entities.user.user import UserId, User


class UserGateway(Protocol):
    def with_id(
        self,
        *,
        user_id: UserId,
    ) -> Optional[User]:
        raise NotImplementedError

    def with_name(
        self,
        *,
        user_name: str,
    ) -> Optional[User]:
        raise NotImplementedError

    def save(
        self,
        *,
        user: User,
    ) -> None:
        raise NotImplementedError

    def update(
        self,
        *,
        user: User,
    ) -> None:
        raise NotImplementedError
