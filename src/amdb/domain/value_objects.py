from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Money:
    value: int
    currency: str


@dataclass(frozen=True, slots=True)
class Date:
    year: int
    month: Optional[int]
    day: Optional[int]


@dataclass(frozen=True, slots=True)
class Title:
    en_title: Optional[str]
    original_title: Optional[str]

    def __post_init__(self) -> None:
        if self.en_title is None and self.original_title is None:
            raise ValueError(
                "Title must at least include en_title or original_title",
            )


@dataclass(frozen=True, slots=True)
class Runtime:
    hours: int
    minutes: int


@dataclass(frozen=True, slots=True)
class Vote:
    value: float

    def __post_init__(self) -> None:
        if 10 < self.value < 0.5 or self.value % 0.5 != 0:
            raise ValueError(
                "Vote's value must be between 0.5 and 10, " "and also be a multiple of 0.5",
            )
