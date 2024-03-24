from typing import Optional

from amdb.domain.entities.user import UserId, User
from amdb.domain.validators.email import ValidateEmail
from amdb.domain.validators.telegram import ValidateTelegram
from amdb.domain.constants.exceptions import INVALID_USER_NAME
from amdb.domain.exception import DomainError


USER_NAME_MIN_LENGTH = 1
USER_NAME_MAX_LENGTH = 128


class CreateUser:
    def __init__(
        self,
        validate_email: ValidateEmail,
        validate_telegram: ValidateTelegram,
    ) -> None:
        self._validate_email = validate_email
        self._validate_telegram = validate_telegram

    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        email: Optional[str],
        telegram: Optional[str],
    ) -> User:
        if email:
            self._validate_email(email)
        if telegram:
            self._validate_telegram(telegram)

        self._validate_name(name)

        return User(
            id=id,
            name=name,
            email=email,
            telegram=telegram,
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
