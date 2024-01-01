from typing import Optional

from sqlalchemy import select, and_, inspect
from sqlalchemy.orm.session import Session

from amdb.domain.entities.user import UserId
from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.rating import Rating as RatingEntity
from amdb.application.common.interfaces.rating_gateway import RatingGateway
from amdb.infrastructure.database.models.rating import Rating as RatingModel
from amdb.infrastructure.database.mappers.rating import RatingMapper


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
        statement = (
            select(RatingModel)
            .where(
                and_(
                    RatingModel.user_id == user_id,
                    RatingModel.movie_id == movie_id,
                ),
            )
        )
        rating_model = self._session.scalar(statement)
        if rating_model:
            return self._mapper.to_entity(
                rating=rating_model,
            )
        return None

    def save(self, rating: RatingEntity) -> None:
        rating_model = self._mapper.to_model(
            rating=rating,
        )
        self._session.add(rating_model)
        self._session.flush((rating_model,))

    def delete(self, rating: RatingEntity) -> None:
        rating_model = self._mapper.to_model(
            rating=rating,
        )
        rating_model_insp = inspect(rating_model)
        if rating_model_insp.persistent:
            self._session.delete(rating_model)
            self._session.flush((rating_model,))
        elif rating_model_insp.pending:
            self._session.expunge(rating_model)
