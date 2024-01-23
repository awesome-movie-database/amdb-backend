from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class Person(Model):
    __tablename__ = "persons"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
