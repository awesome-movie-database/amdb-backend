import re

from amdb.domain.constants.exceptions import INVALID_EMAIL
from amdb.domain.exception import DomainError


class ValidateEmail:
    _REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    def __call__(self, email: str) -> str:
        match = re.fullmatch(self._REGEX, email)
        if not match:
            raise DomainError(INVALID_EMAIL)
        return email
