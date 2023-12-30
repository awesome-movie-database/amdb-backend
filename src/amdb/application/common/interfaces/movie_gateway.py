from typing import Optional, Protocol

from amdb.domain.entities.movie import MovieId, Movie


class MovieGateway(Protocol):
    def with_id(self, movie_id: MovieId) -> Optional[Movie]:
        raise NotImplementedError
    
    def save(self, movie: Movie) -> None:
        raise NotImplementedError
    
    def update(self, movie: Movie) -> None:
        raise NotImplementedError

    def delete(self, movie: Movie) -> None:
        raise NotImplementedError
