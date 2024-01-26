from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model
from .user import User
from .movie import Movie


class Review(Model):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    movie_id: Mapped[UUID] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
    )
    title: Mapped[str]
    content: Mapped[str]
    type: Mapped[int]
    created_at: Mapped[datetime]

    user: Mapped[User] = relationship()
    movie: Mapped[Movie] = relationship()
