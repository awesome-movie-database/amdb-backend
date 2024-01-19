from amdb.domain.entities.user import UserId
from amdb.infrastructure.persistence.sqlalchemy.models.user_permissions import (
    UserPermissions as UserPermissionsModel,
)


class UserPermissionsMapper:
    def to_model(self, user_id: UserId, permissions: int) -> UserPermissionsModel:
        return UserPermissionsModel(
            user_id=user_id,
            permissions=permissions,
        )
