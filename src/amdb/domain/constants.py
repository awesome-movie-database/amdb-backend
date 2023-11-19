from enum import IntEnum


class Unset:
    """
    Сlass needed to identify parameters
    that were not passed.

    Example:

    .. code-block::python
    def foo(bar: Union[int, None Type[Unset]]= Unset):
        if bar == Unset:
            ...
    """


class Sex(IntEnum):

    MALE = 0
    FEMALE = 1


class Genre(IntEnum):

    ACTION = 0
    COMEDY = 1
    DOCUMENTARY = 2
    DRAMA = 3
    FANTASY = 4
    HORROR = 5
    MUSICAL = 6
    MYSTERY = 7
    ROMANCE = 8
    SCIENCE_FICTION = 9
    THRILLER = 10
    WESTERN = 11
    ANIMATION = 12
    ADVENTURE = 13
    ADULT = 14
    BIOGRAPHY = 15
    CRIME = 16
    FAMILY = 17
    NOIR = 18
    SHORT = 19
    SPORT = 20
    WAR = 21
    MUSIC = 22
    HISTORY = 23
    DETECTIVE = 24


class MPAA(IntEnum):

    G = 0
    PG = 1
    PG13 = 2
    R = 3
    NC17 = 4


class ProductionStatus(IntEnum):

    FILMING = 0
    PRE_PRODUCTION = 1
    COMPLETED = 2
    ANNOUNCED = 3
    UNKNOWN = 4
    POST_PRODUCTION = 5


class ReviewType(IntEnum):

    NEUTRAL = 0
    POSITIVE = 1
    NEGATIVE = 2


class RatingType(IntEnum):

    LIKE = 0
    DISLIKE = 1
