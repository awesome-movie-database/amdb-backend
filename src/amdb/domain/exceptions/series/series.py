from amdb.domain.exceptions.base import DomainException


class SeriesUnderInspection(DomainException):
    """
    Operation cannot be performed while series is under inspection
    """


class SeriesNotUnderInspection(DomainException):
    """
    Operation cannot be performed while series is not under inspection
    """
