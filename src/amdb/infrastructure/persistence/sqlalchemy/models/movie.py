from datetime import date
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class MovieModel(Model):
    __tablename__ = "movies"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    title: Mapped[str]
    release_date: Mapped[date]
    rating: Mapped[float]
    rating_count: Mapped[int]
