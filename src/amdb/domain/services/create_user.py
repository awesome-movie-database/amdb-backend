from typing import Optional

from amdb.domain.entities.user import UserId, User
from amdb.domain.validators.email import ValidateEmail


class CreateUser:
    def __init__(
        self,
        validate_email: ValidateEmail,
    ) -> None:
        self._validate_email = validate_email

    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        email: Optional[str],
    ) -> User:
        if email:
            email = self._validate_email(email)
        else:
            email = None

        return User(
            id=id,
            name=name,
            email=email,
        )
