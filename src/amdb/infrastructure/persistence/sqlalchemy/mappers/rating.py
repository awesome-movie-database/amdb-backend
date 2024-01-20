from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import Rating as RatingEntity
from amdb.infrastructure.persistence.sqlalchemy.models.rating import Rating as RatingModel


class RatingMapper:
    def to_model(self, rating: RatingEntity) -> RatingModel:
        return RatingModel(
            movie_id=rating.movie_id,
            user_id=rating.user_id,
            value=rating.value,
            created_at=rating.created_at,
        )

    def to_entity(self, rating: RatingModel) -> RatingEntity:
        return RatingEntity(
            movie_id=MovieId(rating.movie_id),
            user_id=UserId(rating.user_id),
            value=rating.value,
            created_at=rating.created_at,
        )
