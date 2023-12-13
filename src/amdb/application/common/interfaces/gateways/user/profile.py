from typing import Optional, Protocol

from amdb.domain.entities.user.user import UserId
from amdb.domain.entities.user.profile import Profile


class ProfileGateway(Protocol):
    def with_user_id(
        self,
        *,
        user_id: UserId,
    ) -> Optional[Profile]:
        raise NotImplementedError

    def save(
        self,
        *,
        profile: Profile,
    ) -> None:
        raise NotImplementedError

    def update(
        self,
        *,
        profile: Profile,
    ) -> None:
        raise NotImplementedError
