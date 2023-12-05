from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class Date:
    year: int

    month: Optional[int]
    day: Optional[int]

    def __post_init__(self) -> None:
        if self.year <= 0:
            raise ValueError("Date year must be greater than 0")
        elif self.month is not None and 0 >= self.month > 12:
            raise ValueError("Date month must be greater than 0 and less than or equal to 12")
        elif self.day is not None and 0 >= self.day > 31:
            raise ValueError("Date day must be greater than 0 and less than or equal to 31")


@dataclass(frozen=True, slots=True)
class Place:
    country: str

    state: Optional[str]
    city: Optional[str]


@dataclass(frozen=True, slots=True)
class Money:
    value: int
    currency: str

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Money value must be greater than or equal to 0")

    def __le__(self, other: Any) -> bool:
        self._enusre_money(
            obj=other,
        )
        return self.value <= other.value

    def __lt__(self, other: Any) -> bool:
        self._enusre_money(
            obj=other,
        )
        return self.value < other.value

    def __ge__(self, other: Any) -> bool:
        self._enusre_money(
            obj=other,
        )
        return self.value >= other.value

    def __gt__(self, other: Any) -> bool:
        self._enusre_money(
            obj=other,
        )
        return self.value > other.value

    def __add__(self, other: Any) -> "Money":
        self._enusre_money(
            obj=other,
        )
        return Money(
            value=self.value + other.value,
            currency=self.currency,
        )

    def __sub__(self, other: Any) -> "Money":
        self._enusre_money(
            obj=other,
        )
        return Money(
            value=self.value - other.value,
            currency=self.currency,
        )

    def _enusre_money(self, obj: Any) -> None:
        if not isinstance(obj, Money):
            raise ValueError("Object must be instance of `Money`")
        elif obj.currency != self.currency:
            raise ValueError("Money must be the same currency")


@dataclass(frozen=True, slots=True)
class Runtime:
    minutes: int

    def __post_init__(self) -> None:
        if self.minutes <= 0:
            raise ValueError("Runtime minutes must be greater than 0")

    def __add__(self, other: Any) -> "Runtime":
        self._enusre_runtime(
            obj=other,
        )
        return Runtime(
            minutes=self.minutes + other.minutes,
        )

    def __sub__(self, other: Any) -> "Runtime":
        self._enusre_runtime(
            obj=other,
        )
        return Runtime(
            minutes=self.minutes - other.minutes,
        )

    def _enusre_runtime(self, obj: Any) -> None:
        if not isinstance(obj, Runtime):
            raise ValueError("Object must be instance of `Runtime`")


@dataclass(frozen=True, slots=True)
class Rating:
    value: float

    def __post_init__(self) -> None:
        if 0 >= self.value > 10 and self.value % 0.5 != 0:
            raise ValueError(
                "Rating must be greater than 0, less than or equal to 10 and a multiple of 0.5",
            )
