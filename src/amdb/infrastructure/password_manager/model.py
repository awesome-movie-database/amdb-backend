from dataclasses import dataclass

from amdb.domain.entities.user import UserId
from amdb.infrastructure.security.hasher import HashData


@dataclass(frozen=True, slots=True)
class UserPasswordHash:
    user_id: UserId
    password_hash: HashData
