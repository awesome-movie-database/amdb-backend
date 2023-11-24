from .base import DomainException


class AccessDenied(DomainException):
    """
    Operation cannot be performed due to lack of access
    """
