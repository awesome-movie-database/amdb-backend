from typing import Optional

from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.mappers.user_permissions import (
    UserPermissionsMapper,
)
from amdb.infrastructure.persistence.sqlalchemy.models.user_permissions import UserPermissions


class SQLAlchemyPermissionsGateway:
    def __init__(
        self,
        session: Session,
        mapper: UserPermissionsMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_user_id(self, user_id: UserId) -> Optional[int]:
        user_permissions_model = self._session.get(UserPermissions, user_id)
        if user_permissions_model:
            return user_permissions_model.permissions
        return None

    def set(self, user_id: UserId, permissions: int) -> None:
        user_permissions_model = self._mapper.to_model(
            user_id=user_id,
            permissions=permissions,
        )
        self._session.add(user_permissions_model)

    def for_new_user(self) -> int:
        return 4

    def for_create_movie(self) -> int:
        return 2

    def for_delete_movie(self) -> int:
        return 2

    def for_rate_movie(self) -> int:
        return 4

    def for_unrate_movie(self) -> int:
        return 4
