from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Model


class ReviewModel(Model):
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
    type: Mapped[str]
    created_at: Mapped[datetime]
