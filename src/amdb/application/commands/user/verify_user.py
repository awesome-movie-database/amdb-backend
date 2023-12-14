from dataclasses import dataclass

from amdb.domain.entities.user.user import UserId


@dataclass(frozen=True, slots=True)
class VerifyUserCommand:
    user_id: UserId
