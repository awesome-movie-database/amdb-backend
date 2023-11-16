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
