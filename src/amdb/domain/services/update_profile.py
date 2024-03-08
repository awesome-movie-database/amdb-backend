from typing import Optional

from amdb.domain.entities.user import User
from amdb.domain.validators.email import ValidateEmail


class UpdateProfile:
    def __init__(
        self,
        validate_email: ValidateEmail,
    ) -> None:
        self._validate_email = validate_email

    def __call__(
        self,
        *,
        user: User,
        email: Optional[str],
    ) -> None:
        if email:
            self._validate_email(email)
        user.email = email
