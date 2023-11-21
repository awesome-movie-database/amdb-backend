from amdb.domain.exceptions.base import DomainException


class SeriesSeasonUnderInspection(DomainException):
    """
    Operation cannot be performed while series season is under inspection
    """


class SeriesSeasonNotUnderInspection(DomainException):
    """
    Operation cannot be performed while series season is not under inspection
    """
