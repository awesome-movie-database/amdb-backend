from dataclasses import dataclass

from amdb.domain.entities.user import UserId
from .hasher import PasswordHash


@dataclass(frozen=True, slots=True)
class UserPasswordHash:
    user_id: UserId
    password_hash: PasswordHash
