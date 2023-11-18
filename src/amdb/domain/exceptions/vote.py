from .base import DomainException


class NotEnoughAmdbVotes(DomainException):
    """
    Operation cannot be performed beacause movie or series
    has not enough amdb votes
    """
