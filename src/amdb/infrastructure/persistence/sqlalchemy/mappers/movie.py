from amdb.domain.entities.movie import MovieId, Movie as MovieEntity
from amdb.infrastructure.persistence.sqlalchemy.models.movie import Movie as MovieModel


class MovieMapper:
    def to_model(self, movie: MovieEntity) -> MovieModel:
        return MovieModel(
            id=movie.id,
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            rating_count=movie.rating_count,
        )

    def to_entity(self, movie: MovieModel) -> MovieEntity:
        return MovieEntity(
            id=MovieId(movie.id),
            title=movie.title,
            release_date=movie.release_date,
            rating=movie.rating,
            rating_count=movie.rating_count,
        )
