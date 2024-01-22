from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from amdb.domain.entities.movie import MovieId, Movie as MovieEntity
from amdb.infrastructure.persistence.sqlalchemy.models.movie import Movie as MovieModel
from amdb.infrastructure.persistence.sqlalchemy.mappers.movie import MovieMapper


class SQLAlchemyMovieGateway:
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
            return self._mapper.to_entity(movie_model)
        return None

    def save(self, movie: MovieEntity) -> None:
        movie_model = self._mapper.to_model(movie)
        self._session.add(movie_model)

    def update(self, movie: MovieEntity) -> None:
        movie_model = self._mapper.to_model(movie)
        self._session.merge(movie_model)

    def delete(self, movie: MovieEntity) -> None:
        movie_model = self._session.get(MovieModel, movie.id)
        if movie_model:
            self._session.delete(movie_model)

    def list(self, limit: int, offset: int) -> list[MovieEntity]:
        statement = select(MovieModel).limit(limit).offset(offset)
        movie_models = self._session.scalars(statement)

        movie_entities = []
        for movie_model in movie_models:
            movie_entity = self._mapper.to_entity(movie_model)
            movie_entities.append(movie_entity)

        return movie_entities
