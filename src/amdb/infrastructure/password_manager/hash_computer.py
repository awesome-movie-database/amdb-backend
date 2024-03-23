import hashlib


ALGORITHM = "sha256"
ITERATIONS = 10000


class HashComputer:
    def hash(self, value: bytes, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            hash_name=ALGORITHM,
            password=value,
            salt=salt,
            iterations=ITERATIONS,
        )

    def verify(
        self,
        value: bytes,
        hashed_value: bytes,
        salt: bytes,
    ) -> bool:
        computed_hash = hashlib.pbkdf2_hmac(
            hash_name=ALGORITHM,
            password=value,
            salt=salt,
            iterations=ITERATIONS,
        )
        return computed_hash == hashed_value
