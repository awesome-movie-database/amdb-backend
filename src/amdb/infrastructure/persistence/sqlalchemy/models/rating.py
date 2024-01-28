from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model
from .user import User
from .movie import Movie


class Rating(Model):
    __tablename__ = "ratings"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    movie_id: Mapped[UUID] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    value: Mapped[float]
    created_at: Mapped[datetime]

    movie: Mapped[Movie] = relationship()
    user: Mapped[User] = relationship()

    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)
