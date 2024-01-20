from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class Movie(Model):
    __tablename__ = "movies"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    title: Mapped[str]
    rating: Mapped[float]
    rating_count: Mapped[int]
