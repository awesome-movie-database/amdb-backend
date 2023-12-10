from datetime import date, datetime
from typing import Optional

from amdb.domain.services.base import Service
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.constants import Sex
from amdb.domain.value_objects import Place


class CreateUser(Service):
    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        password: str,
        timestamp: datetime,
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
            created_at=timestamp,
            email=email,
            sex=sex,
            birth_date=birth_date,
            location=location,
            verified_at=None,
            updated_at=None,
        )
