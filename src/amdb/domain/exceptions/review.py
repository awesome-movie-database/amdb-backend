from .base import DomainError


class MovieReviewNotApprovedError(DomainError):
    ...


class SeriesNotApprovedError(DomainError):
    ...


class SeriesSeasonReviewNotApprovedError(DomainError):
    ...


class SeriesEpisodeReviewNotApprovedError(DomainError):
    ...
