from .base import DomainError


class MovieReviewNotApprovedError(DomainError):
    ...


class SeriesReviewNotApprovedError(DomainError):
    ...


class SeriesSeasonReviewNotApprovedError(DomainError):
    ...


class SeriesEpisodeReviewNotApprovedError(DomainError):
    ...
