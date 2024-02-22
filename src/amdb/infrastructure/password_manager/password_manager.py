import os

from amdb.domain.entities.user import UserId
from amdb.infrastructure.exception import InfrastructureError
from .password_hash import PasswordHash
from .password_hash_gateway import PasswordHashGateway
from .hash_computer import HashComputer


PASSWORD_HASH_DOES_NOT_EXIST = "Password hash doesn't exist"


class HashingPasswordManager:
    def __init__(
        self,
        hash_computer: HashComputer,
        password_hash_gateway: PasswordHashGateway,
    ) -> None:
        self._hash_computer = hash_computer
        self._password_hash_gateway = password_hash_gateway

    def set(self, user_id: UserId, password: str) -> None:
        salt = self._gen_random_bytes()
        hash = self._hash_computer.hash(
            value=password.encode(),
            salt=salt,
        )
        password_hash = PasswordHash(
            user_id=user_id,
            hash=hash,
            salt=salt,
        )
        self._password_hash_gateway.save(password_hash)

    def verify(self, user_id: UserId, password: str) -> bool:
        password_hash = self._password_hash_gateway.with_user_id(user_id)
        if not password_hash:
            raise InfrastructureError(PASSWORD_HASH_DOES_NOT_EXIST)

        return self._hash_computer.verify(
            value=password.encode(),
            hashed_value=password_hash.hash,
            salt=password_hash.salt,
        )

    def _gen_random_bytes(self) -> bytes:
        return os.urandom(32)
