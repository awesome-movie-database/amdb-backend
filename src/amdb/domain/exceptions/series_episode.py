from amdb.domain.exceptions.base import DomainException


class SeriesEpisodeUnderInspection(DomainException):
    """
    Operation cannot be performed while series episode is under inspection
    """


class SeriesEpisodeNotUnderInspection(DomainException):
    """
    Operation cannot be performed while series episode is not under inspection
    """
