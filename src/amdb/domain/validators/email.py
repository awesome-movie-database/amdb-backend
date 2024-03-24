import re

from amdb.domain.constants.exceptions import INVALID_EMAIL
from amdb.domain.exception import DomainError


PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")


class ValidateEmail:
    def __call__(self, email: str) -> None:
        match = re.fullmatch(PATTERN, email)
        if not match:
            raise DomainError(INVALID_EMAIL)
