from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from amdb.infrastructure.database.models.base import Model


class Profile(Model):
    __tablename__ = "profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    achievements: Mapped[int]
    movie_ratings: Mapped[int]
    series_episode_ratings: Mapped[int]
    approved_reviews: Mapped[int]
    movie_reviews: Mapped[int]
    series_reviews: Mapped[int]
    series_season_reviews: Mapped[int]
    series_episode_reviews: Mapped[int]
    given_votes: Mapped[int]
    gained_votes: Mapped[int]
