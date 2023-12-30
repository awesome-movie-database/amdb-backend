from amdb.domain.entities.movie import MovieId, Movie


class CreateMovie:
    def __call__(
        self,
        *,
        id: MovieId,
        title: str,
    ) -> Movie:
        return Movie(
            id=id,
            title=title,
            rating=0,
            rating_count=0,
        )
