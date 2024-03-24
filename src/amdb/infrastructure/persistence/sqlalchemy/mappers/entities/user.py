from typing import Annotated, Optional

from sqlalchemy import Connection, Row, select, insert, update

from amdb.domain.entities.user import UserId, User
from amdb.infrastructure.persistence.sqlalchemy.models.user import UserModel


class UserMapper:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def with_id(self, user_id: UserId) -> Optional[User]:
        statement = select(UserModel).where(UserModel.id == user_id)
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def with_name(self, user_name: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.name == user_name)
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def with_email(self, user_email: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.email == user_email)
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def with_telegram(self, user_telegram: str) -> Optional[User]:
        statement = select(UserModel).where(
            UserModel.telegram == user_telegram,
        )
        row = self._connection.execute(statement).one_or_none()
        if row:
            return self._to_entity(row)  # type: ignore
        return None

    def save(self, user: User) -> None:
        statement = insert(UserModel).values(
            id=UserId(user.id),
            name=user.name,
            email=user.email,
            telegram=user.telegram,
        )
        self._connection.execute(statement)

    def update(self, user: User) -> None:
        statement = update(UserModel).values(email=user.email)
        self._connection.execute(statement)

    def _to_entity(
        self,
        row: Annotated[UserModel, Row],
    ) -> User:
        return User(
            id=UserId(row.id),
            name=row.name,
            email=row.email,
            telegram=row.telegram,
        )
