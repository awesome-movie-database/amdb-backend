from amdb.domain.constants.exceptions import INVALID_TELEGRAM
from amdb.domain.exception import DomainError


TELEGRAM_MIN_LENGTH = 5
TELEGRAM_MAX_LENGTH = 32


class ValidateTelegram:
    def __call__(self, telegram: str) -> None:
        telegram_length = len(telegram)
        if (
            telegram_length < TELEGRAM_MIN_LENGTH
            or telegram_length > TELEGRAM_MAX_LENGTH
        ):
            raise DomainError(INVALID_TELEGRAM)

        for character in telegram:
            if not character.isalnum() and character != "_":
                raise DomainError(INVALID_TELEGRAM)
