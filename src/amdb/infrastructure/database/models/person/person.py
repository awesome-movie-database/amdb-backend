from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from amdb.infrastructure.database.models.base import Model


class Person(Model):
    __tablename__ = "persons"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    sex: Mapped[int]
    created_at: Mapped[datetime]
    birth_year: Mapped[Optional[int]]
    birth_month: Mapped[Optional[int]]
    birth_day: Mapped[Optional[int]]
    birth_country: Mapped[Optional[str]]
    birth_state: Mapped[Optional[str]]
    birth_city: Mapped[Optional[str]]
    death_year: Mapped[Optional[int]]
    death_month: Mapped[Optional[int]]
    death_day: Mapped[Optional[int]]
    death_country: Mapped[Optional[str]]
    death_state: Mapped[Optional[str]]
    death_city: Mapped[Optional[str]]
    updated_at: Mapped[Optional[datetime]]
