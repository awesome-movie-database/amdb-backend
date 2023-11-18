from .base import DomainException


class PersonUnderInspection(DomainException):
    """
    Operation cannot be performed while person is under inspection
    """


class PersonNotUnderInspection(DomainException):
    """
    Operation cannot be performed while person is not under inspection
    """