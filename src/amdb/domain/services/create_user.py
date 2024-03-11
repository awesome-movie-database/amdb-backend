from typing import Optional

from amdb.domain.entities.user import UserId, User
from amdb.domain.validators.email import ValidateEmail
from amdb.domain.constants.exceptions import INVALID_USER_NAME
from amdb.domain.exception import DomainError


USER_NAME_MIN_LENGTH = 1
USER_NAME_MAX_LENGTH = 128


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

        self._validate_name(name)

        return User(
            id=id,
            name=name,
            email=email,
        )

    def _validate_name(self, name: str) -> None:
        name_length = len(name)
        name_has_spaces = len(name.split()) != 1
        if (
            name_length < USER_NAME_MIN_LENGTH
            or name_length > USER_NAME_MAX_LENGTH
            or name_has_spaces
        ):
            raise DomainError(INVALID_USER_NAME)
