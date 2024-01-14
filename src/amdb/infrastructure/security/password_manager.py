from typing import cast

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.gateways.user_password import (
    SQLAlchemyUserPasswordHashGateway,
)
from .hasher import Hasher
from .model import UserPasswordHash


class HashingPasswordManager:
    def __init__(
        self,
        hasher: Hasher,
        user_password_hash_gateway: SQLAlchemyUserPasswordHashGateway,
    ) -> None:
        self._hasher = hasher
        self._user_password_hash_gateway = user_password_hash_gateway

    def set(self, user_id: UserId, password: str) -> None:
        password_hash = self._hasher.hash(password)
        user_password_hash = UserPasswordHash(user_id, password_hash)
        self._user_password_hash_gateway.save(user_password_hash)

    def verify(self, user_id: UserId, password: str) -> bool:
        user_password_hash = self._user_password_hash_gateway.get(user_id)
        user_password_hash = cast(UserPasswordHash, user_password_hash)
        return self._hasher.verify(password, user_password_hash.password_hash)
