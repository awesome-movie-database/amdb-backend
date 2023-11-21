from amdb.domain.exceptions.base import DomainException


class SeriesEpisodeUnderInspection(DomainException):
    """
    Operation cannot be performed while series episode is under inspection
    """
