from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class MovieForLaterModel(Model):
    __tablename__ = "movies_for_later"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    movie_id: Mapped[UUID] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
    )
    note: Mapped[str]
    created_at: Mapped[datetime]

    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)
