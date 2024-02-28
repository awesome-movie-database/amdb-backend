from typing import Optional

from amdb.domain.entities.user import User


class UpdateProfile:
    def __call__(
        self,
        *,
        user: User,
        email: Optional[str],
    ) -> None:
        user.email = email
