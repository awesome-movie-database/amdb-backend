from amdb.domain.entities.user import UserId, User


class CreateUser:
    def __call__(
        self,
        *,
        id: UserId,
        name: str,
    ) -> User:
        return User(
            id=id,
            name=name,
        )
