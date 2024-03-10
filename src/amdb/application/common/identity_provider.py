from typing import Protocol, Optional

from amdb.domain.entities.user import UserId


class IdentityProvider(Protocol):
    def user_id(self) -> UserId:
        """
        Returns current user id if authenticated,
        otherwise raises error
        """
        raise NotImplementedError

    def user_id_or_none(self) -> Optional[UserId]:
        """
        Returns current user id if authenticated,
        otherwise returns None
        """
        raise NotImplementedError

    def permissions(self) -> int:
        """
        Returns current user permissions if authenticated,
        otherwise raises error
        """
        raise NotImplementedError
