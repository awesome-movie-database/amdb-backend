from enum import Enum, IntEnum


Unset = Enum("Unset", ["unset"])
unset = Unset.unset


class Sex(IntEnum):
    MALE = 0
    FEMALE = 1
