from .base import DomainException


class MovieUnderInspection(DomainException):
    """
    Operation cannot be performed while movie is under inspection
    """


class MovieNotUnderInspection(DomainException):
    """
    Operation cannot be performed while movie is not under inspection
    """
