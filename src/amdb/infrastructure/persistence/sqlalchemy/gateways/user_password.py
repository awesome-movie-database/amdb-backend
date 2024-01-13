from typing import Optional

from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.models.user_password import (
    UserPasswordHash as UserPasswordHashModel,
)
from amdb.infrastructure.persistence.sqlalchemy.mappers.user_password import UserPasswordHashMapper
from amdb.infrastructure.security.model import UserPasswordHash


class SQLAlchemyUserPasswordHashGateway:
    def __init__(
        self,
        session: Session,
        mapper: UserPasswordHashMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def get(self, user_id: UserId) -> Optional[UserPasswordHash]:
        user_password_hash_model = self._session.get(UserPasswordHashModel, user_id)
        if user_password_hash_model:
            return self._mapper.to_password_manager_model(user_password_hash_model)
        return None

    def save(self, user_password_hash: UserPasswordHash) -> None:
        user_password_hash_model = self._mapper.to_model(user_password_hash)
        self._session.add(user_password_hash_model)
        self._session.commit()
