from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, ReviewType, Review as ReviewEntity
from amdb.infrastructure.persistence.sqlalchemy.models.review import Review as ReviewModel


class ReviewMapper:
    def to_model(self, review: ReviewEntity) -> ReviewModel:
        return ReviewModel(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            title=review.title,
            content=review.content,
            type=review.type.value,
            created_at=review.created_at,
        )

    def to_entity(self, review: ReviewModel) -> ReviewEntity:
        return ReviewEntity(
            id=ReviewId(review.id),
            user_id=UserId(review.user_id),
            movie_id=MovieId(review.movie_id),
            title=review.title,
            content=review.content,
            type=ReviewType(review.type),
            created_at=review.created_at,
        )
