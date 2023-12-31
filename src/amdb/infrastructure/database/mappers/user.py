from amdb.domain.entities.user import UserId, User as UserEntity
from amdb.infrastructure.database.models.user import User as UserModel


class UserMapper:
    def to_model(self, user: UserEntity) -> UserModel:
        return UserModel(
            id=user.id,
            name=user.name,
        )
    
    def to_entity(self, user: UserModel) -> UserEntity:
        return UserEntity(
            id=UserId(user.id),
            name=user.name,
        )
