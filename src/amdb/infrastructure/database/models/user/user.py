from datetime import datetime, date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from amdb.infrastructure.database.models.base import Model


class User(Model):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )
    password: Mapped[str]
    is_active: Mapped[bool]
    is_verified: Mapped[bool]
    created_at: Mapped[datetime]
    email: Mapped[Optional[str]]
    sex: Mapped[Optional[int]]
    birth_date: Mapped[Optional[date]]
    country: Mapped[Optional[str]]
    state: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    verified_at: Mapped[Optional[datetime]]
    updated_at: Mapped[Optional[datetime]]
