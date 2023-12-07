from datetime import date, datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import UserId, UserName, User
from amdb.domain.constants import Sex
from amdb.domain.value_objects import Place


class CreateUser(Service):
    def __call__(
        self,
        *,
        id: UserId,
        name: UserName,
        password: str,
        created_at: datetime,
        email: Optional[str] = None,
        sex: Optional[Sex] = None,
        birth_date: Optional[date] = None,
        location: Optional[Place] = None,
    ) -> User:
        return User(
            id=id,
            name=name,
            password=password,
            is_active=True,
            is_verified=False,
            created_at=created_at,
            email=email,
            sex=sex,
            birth_date=birth_date,
            location=location,
            verified_at=None,
            updated_at=None,
        )
