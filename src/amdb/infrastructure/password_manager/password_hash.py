from dataclasses import dataclass

from amdb.domain.entities.user import UserId


@dataclass(frozen=True, slots=True)
class PasswordHash:
    user_id: UserId
    hash: bytes
    salt: bytes
