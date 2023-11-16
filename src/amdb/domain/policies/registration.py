from dataclasses import dataclass
from datetime import date

from amdb.domain.exceptions.registration import RegistrationDenied
from .base import Policy


@dataclass(slots=True)
class RegistrationPolicy(Policy):

    auto_verify: bool
    valid_age: int

    def ensure_valid_age(self, birth_date: date) -> None:
        if birth_date.year < self.valid_age:
            message = (
                "Valid age is {}, but {} was given".
                format(self.valid_age, birth_date.year)
            )
            raise RegistrationDenied(message)