from amdb.infrastructure.persistence.sqlalchemy.models.user_password import (
    UserPasswordHash as UserPasswordHashModel,
)
from amdb.infrastructure.security.hasher import PasswordHash
from amdb.infrastructure.security.model import UserPasswordHash


class UserPasswordHashMapper:
    def to_model(
        self,
        user_password_hash: UserPasswordHash,
    ) -> UserPasswordHashModel:
        return UserPasswordHashModel(
            user_id=user_password_hash.user_id,
            hash=user_password_hash.password_hash.hash,
            salt=user_password_hash.password_hash.salt,
        )

    def to_password_manager_model(
        self,
        user_password_hash: UserPasswordHashModel,
    ) -> UserPasswordHash:
        password_hash = PasswordHash(
            hash=user_password_hash.hash,
            salt=user_password_hash.salt,
        )
        return UserPasswordHash(
            user_id=user_password_hash.user_id,
            password_hash=password_hash,
        )
