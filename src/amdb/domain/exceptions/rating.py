from .base import DomainError


class MovieRatingAlreadyCountedError(DomainError):
    ...


class SeriesEpisodeRatingAlreadyCountedError(DomainError):
    ...
