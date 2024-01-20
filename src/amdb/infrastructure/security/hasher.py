import os
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HashData:
    hash: bytes
    salt: bytes


class Hasher:
    def hash(self, value: bytes) -> HashData:
        salt = os.urandom(32)
        hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=value,
            salt=salt,
            iterations=10000,
        )
        return HashData(hash=hash, salt=salt)

    def verify(self, value: bytes, hash_data: HashData) -> bool:
        hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=value,
            salt=hash_data.salt,
            iterations=10000,
        )
        return hash == hash_data.hash
