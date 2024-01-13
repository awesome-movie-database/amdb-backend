from typing import Optional

from sqlalchemy import delete
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import Rating as RatingEntity
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.infrastructure.persistence.sqlalchemy.models.rating import Rating as RatingModel
from amdb.infrastructure.persistence.sqlalchemy.mappers.rating import RatingMapper


class SQLAlchemyRatingGateway(RatingGateway):
    def __init__(
        self,
        session: Session,
        mapper: RatingMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[RatingEntity]:
        rating_model = self._session.get(
            RatingModel,
            {"user_id": user_id, "movie_id": movie_id},
        )
        if rating_model:
            return self._mapper.to_entity(rating_model)
        return None

    def save(self, rating: RatingEntity) -> None:
        rating_model = self._mapper.to_model(rating)
        self._session.add(rating_model)

    def delete(self, rating: RatingEntity) -> None:
        rating_model = self._session.get(
            RatingModel,
            {"user_id": rating.user_id, "movie_id": rating.movie_id},
        )
        if rating_model:
            self._session.delete(rating_model)

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        statement = delete(RatingModel).where(RatingModel.movie_id == movie_id)
        self._session.execute(statement)
