from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert

from amdb.domain.entities.user import UserId
from amdb.infrastructure.password_manager.password_hash import PasswordHash
from amdb.infrastructure.persistence.sqlalchemy.models.password_hash import (
    PasswordHashModel,
)


class PasswordHashMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_user_id(self, user_id: UserId) -> Optional[PasswordHash]:
        statement = select(PasswordHashModel).where(
            PasswordHashModel.user_id == user_id,
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_data_structure(row)  # type: ignore
        return None

    def save(self, password_hash: PasswordHash) -> None:
        statement = insert(PasswordHashModel).values(
            user_id=password_hash.user_id,
            hash=password_hash.hash,
            salt=password_hash.salt,
        )
        self._connection.execute(statement)

    def _to_data_structure(
        self,
        row: Annotated[PasswordHashModel, Row],
    ) -> PasswordHash:
        return PasswordHash(
            user_id=UserId(row.user_id),
            hash=row.hash,
            salt=row.salt,
        )
