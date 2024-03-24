from typing import Optional, Union

from amdb.domain.entities.user import User
from amdb.domain.validators.email import ValidateEmail
from amdb.domain.validators.telegram import ValidateTelegram
from amdb.domain.unset import UNSET_T, UNSET


class UpdateProfile:
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
        user: User,
        email: Union[str, None, UNSET_T] = UNSET,
        telegram: Union[str, None, UNSET_T] = UNSET,
    ) -> None:
        if email is not UNSET:
            self._update_email(user, email)
        if telegram is not UNSET:
            self._update_telegram(user, telegram)

    def _update_email(
        self,
        user: User,
        email: Optional[str],
    ) -> None:
        if email:
            self._validate_email(email)
        user.email = email

    def _update_telegram(
        self,
        user: User,
        telegram: Optional[str],
    ) -> None:
        if telegram:
            self._validate_telegram(telegram)
        user.telegram = telegram
