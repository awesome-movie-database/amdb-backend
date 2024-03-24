from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class UserModel(Model):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )
    email: Mapped[Optional[str]] = mapped_column(
        unique=True,
    )
    telegram: Mapped[Optional[str]] = mapped_column(
        unique=True,
    )
