from dataclasses import dataclass
from uuid import UUID

from .base import Entity


@dataclass(slots=True)
class Reviewer(Entity):

    id: UUID
    user_id: UUID
    folders: int
    movies_ratings: int
    movies_reviews: int
    series_ratings: int
    series_reviews: int
    subscriptions: int
    subscribers: int
    achievements: int

    @classmethod
    def create(cls, id: UUID, user_id: UUID,) -> "Reviewer":
        return Reviewer(
            id=id, user_id=user_id, folders=0, movies_ratings=0,
            movies_reviews=0, series_ratings=0, series_reviews=0,
            subscriptions=0, subscribers=0, achievements=0,
        )

    def add_folder(self) -> None:
        self.folders += 1

    def remove_folder(self) -> None:
        self.folders -= 1

    def add_movie_rating(self) -> None:
        self.movies_ratings += 1

    def remove_movie_rating(self) -> None:
        self.movies_ratings -= 1

    def add_movie_review(self) -> None:
        self.movies_reviews += 1

    def remove_movie_review(self) -> None:
        self.movies_reviews -= 1

    def add_series_rating(self) -> None:
        self.movies_ratings += 1

    def remove_series_rating(self) -> None:
        self.movies_ratings -= 1

    def add_series_review(self) -> None:
        self.movies_reviews += 1

    def remove_series_review(self) -> None:
        self.movies_reviews -= 1

    def add_subscription(self) -> None:
        self.subscriptions += 1

    def remove_subscription(self) -> None:
        self.subscriptions -= 1

    def add_subscriber(self) -> None:
        self.subscribers += 1

    def remove_subscriber(self) -> None:
        self.subscribers -= 1

    def add_achievement(self) -> None:
        self.achievements += 1

    def remove_achievement(self) -> None:
        self.achievements -= 1
