from typing import Optional

from sqlalchemy import inspect
from sqlalchemy.orm.session import Session

from amdb.domain.entities.movie import MovieId, Movie as MovieEntity
from amdb.application.common.interfaces.movie_gateway import MovieGateway
from amdb.infrastructure.database.models.movie import Movie as MovieModel
from amdb.infrastructure.database.mappers.movie import MovieMapper


class SQLAlchemyMovieGateway(MovieGateway):
    def __init__(
        self,
        session: Session,
        mapper: MovieMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    def with_id(self, movie_id: MovieId) -> Optional[MovieEntity]:
        movie_model = self._session.get(MovieModel, movie_id)
        if movie_model:
            return self._mapper.to_entity(
                movie=movie_model,
            )
        return None

    def save(self, movie: MovieEntity) -> None:
        movie_model = self._mapper.to_model(
            movie=movie,
        )
        self._session.add(movie_model)
        self._session.flush((movie_model,))

    def update(self, movie: MovieEntity) -> None:
        movie_model = self._mapper.to_model(
            movie=movie,
        )
        self._session.merge(movie_model)
        self._session.flush((movie_model,))

    def delete(self, movie: MovieEntity) -> None:
        movie_model = self._mapper.to_model(
            movie=movie,
        )
        movie_model_insp = inspect(movie_model)
        if movie_model_insp.persistent:
            self._session.delete(movie_model)
            self._session.flush((movie_model,))
        elif movie_model_insp.pending:
            self._session.expunge(movie_model)
