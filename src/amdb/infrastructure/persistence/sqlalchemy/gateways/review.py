from typing import Optional

from sqlalchemy import select, delete, and_
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, Review as ReviewEntity
from amdb.infrastructure.persistence.sqlalchemy.models.review import Review as ReviewModel
from amdb.infrastructure.persistence.sqlalchemy.mappers.review import ReviewMapper


class SQLAlchemyReviewGateway:
    def __init__(
        self,
        session: Session,
        mapper: ReviewMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(self, review_id: ReviewId) -> Optional[ReviewEntity]:
        review_model = self._session.get(ReviewModel, review_id)
        if review_model:
            return self._mapper.to_entity(review_model)
        return None

    def with_movie_id_and_user_id(
        self,
        user_id: UserId,
        movie_id: MovieId,
    ) -> Optional[ReviewEntity]:
        statement = select(ReviewModel).where(
            and_(
                ReviewModel.user_id == user_id,
                ReviewModel.movie_id == movie_id,
            ),
        )
        review_model = self._session.scalar(statement)
        if review_model:
            return self._mapper.to_entity(review_model)
        return None

    def list_with_movie_id(
        self,
        movie_id: MovieId,
        limit: int,
        offset: int,
    ) -> list[ReviewEntity]:
        statement = (
            select(ReviewModel).where(ReviewModel.movie_id == movie_id).limit(limit).offset(offset)
        )
        review_models = self._session.scalars(statement)

        review_entities = []
        for review_model in review_models:
            review_entity = self._mapper.to_entity(review_model)
            review_entities.append(review_entity)

        return review_entities

    def list_with_user_id(
        self,
        user_id: UserId,
        limit: int,
        offset: int,
    ) -> list[ReviewEntity]:
        statement = (
            select(ReviewModel).where(ReviewModel.user_id == user_id).limit(limit).offset(offset)
        )
        review_models = self._session.scalars(statement)

        review_entities = []
        for review_model in review_models:
            review_entity = self._mapper.to_entity(review_model)
            review_entities.append(review_entity)

        return review_entities

    def save(self, review: ReviewEntity) -> None:
        review_model = self._mapper.to_model(review)
        self._session.add(review_model)

    def delete_with_movie_id(self, movie_id: MovieId) -> None:
        statement = delete(ReviewModel).where(ReviewModel.movie_id == movie_id)
        self._session.execute(statement)
