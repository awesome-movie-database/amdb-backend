from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import User
from amdb.domain.exceptions.user import UserAlreadyVerifiedError


class VerifyUser(Service):
    def __call__(
        self,
        *,
        user: User,
        timestamp: datetime,
    ) -> None:
        if user.is_verified:
            raise UserAlreadyVerifiedError()
        user.verified_at = timestamp
