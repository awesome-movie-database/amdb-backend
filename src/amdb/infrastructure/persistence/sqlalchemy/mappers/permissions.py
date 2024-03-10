from typing import Optional

from sqlalchemy import Connection, Row, select, insert

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.models.permissions import (
    PermissionsModel,
)


class PermissionsMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_user_id(self, user_id: UserId) -> Optional[int]:
        statement = select(PermissionsModel).where(
            PermissionsModel.user_id == user_id,
        )
        row: Optional[Row[tuple[PermissionsModel]]] = self._connection.execute(
            statement,
        ).one_or_none()
        if row is not None:
            return row.value
        return None

    def set(self, user_id: UserId, permissions: int) -> None:
        statement = insert(PermissionsModel).values(
            user_id=user_id,
            value=permissions,
        )
        self._connection.execute(statement)
