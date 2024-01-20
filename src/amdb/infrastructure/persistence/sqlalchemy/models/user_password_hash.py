from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class UserPasswordHash(Model):
    __tablename__ = "user_password_hashes"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    hash: Mapped[bytes]
    salt: Mapped[bytes]
