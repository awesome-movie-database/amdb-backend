import hashlib


class HashComputer:
    _ALGORITHM = "sha256"
    _ITERATIONS = 10000

    def hash(self, value: bytes, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            hash_name=self._ALGORITHM,
            password=value,
            salt=salt,
            iterations=self._ITERATIONS,
        )

    def verify(
        self,
        value: bytes,
        hashed_value: bytes,
        salt: bytes,
    ) -> bool:
        computed_hash = hashlib.pbkdf2_hmac(
            hash_name=self._ALGORITHM,
            password=value,
            salt=salt,
            iterations=self._ITERATIONS,
        )
        return computed_hash == hashed_value
