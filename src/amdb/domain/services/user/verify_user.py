from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import User
from amdb.domain.constants.exceptions import USER_ALREADY_VERIFIED
from amdb.domain.exception import DomainError


class VerifyUser(Service):
    def __call__(
        self,
        *,
        user: User,
        timestamp: datetime,
    ) -> None:
        if user.is_verified:
            raise DomainError(USER_ALREADY_VERIFIED)
        user.verified_at = timestamp
