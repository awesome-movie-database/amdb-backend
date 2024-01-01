from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId, User as UserEntity
from amdb.application.common.interfaces.user_gateway import UserGateway
from amdb.infrastructure.database.models.user import User as UserModel
from amdb.infrastructure.database.mappers.user import UserMapper


class SQLAlchemyUserGateway(UserGateway):
    def __init__(
        self,
        session: Session,
        mapper: UserMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(self, user_id: UserId) -> Optional[UserEntity]:
        user_model = self._session.get(UserModel, user_id)
        if user_model:
            return self._mapper.to_entity(
                user=user_model,
            )
        return None

    def with_name(self, user_name: str) -> Optional[UserEntity]:
        statement = select(UserModel).where(UserModel.name == user_name)
        user_model = self._session.scalar(statement)
        if user_model:
            return self._mapper.to_entity(
                user=user_model,
            )
        return None

    def save(self, user: UserEntity) -> None:
        user_model = self._mapper.to_model(
            user=user,
        )
        self._session.add(user_model)
        self._session.flush((user_model,))
