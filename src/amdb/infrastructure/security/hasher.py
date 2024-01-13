import os
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PasswordHash:
    hash: bytes
    salt: bytes


class Hasher:
    def hash(self, password: str) -> PasswordHash:
        salt = os.urandom(32)
        hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode(),
            salt=salt,
            iterations=10000,
        )
        return PasswordHash(hash=hash, salt=salt)

    def verify(self, password: str, hashed_password: PasswordHash) -> bool:
        hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode(),
            salt=hashed_password.salt,
            iterations=10000,
        )
        return hash == hashed_password.hash
