from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class Rating(Model):
    __tablename__ = "ratings"

    movie_id: Mapped[UUID] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    value: Mapped[float]
    created_at: Mapped[datetime]

    __table_args__ = (PrimaryKeyConstraint(movie_id, user_id),)
