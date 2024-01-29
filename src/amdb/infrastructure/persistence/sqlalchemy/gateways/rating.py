from typing import Optional

from sqlalchemy import select, delete, and_
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import RatingId, Rating as RatingEntity
from amdb.infrastructure.persistence.sqlalchemy.models.rating import Rating as RatingModel
from amdb.infrastructure.persistence.sqlalchemy.mappers.rating import RatingMapper


class SQLAlchemyRatingGateway:
    def __init__(
        self,
        session: Session,
        mapper: RatingMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(self, id: RatingId) -> Optional[RatingEntity]:
        rating_model = self._session.get(RatingModel, id)
        if rating_model:
            return self._mapper.to_entity(rating_model)
        return None

    def with_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[RatingEntity]:
        statement = select(RatingModel).where(
            and_(RatingModel.user_id == user_id, RatingModel.movie_id == movie_id),
        )
        rating_model = self._session.scalar(statement)
        if rating_model:
            return self._mapper.to_entity(rating_model)
        return None

    def list_with_movie_id(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[RatingEntity]:
        statement = (
            select(RatingModel).where(RatingModel.movie_id == movie_id).limit(limit).offset(offset)
        )
        rating_models = self._session.scalars(statement)

        rating_entities = []
        for rating_model in rating_models:
            rating_entity = self._mapper.to_entity(rating_model)
            rating_entities.append(rating_entity)

        return rating_entities

    def list_with_user_id(
        self,
        user_id: UserId,
        limit: int,
        offset: int,
    ) -> list[RatingEntity]:
        statement = (
            select(RatingModel).where(RatingModel.user_id == user_id).limit(limit).offset(offset)
        )
        rating_models = self._session.scalars(statement)

        rating_entities = []
        for rating_model in rating_models:
            rating_entity = self._mapper.to_entity(rating_model)
            rating_entities.append(rating_entity)

        return rating_entities

    def save(self, rating: RatingEntity) -> None:
        rating_model = self._mapper.to_model(rating)
        self._session.add(rating_model)

    def delete(self, rating: RatingEntity) -> None:
        rating_model = self._session.get(RatingModel, rating.id)
        if rating_model:
            self._session.delete(rating_model)

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        statement = delete(RatingModel).where(RatingModel.movie_id == movie_id)
        self._session.execute(statement)
