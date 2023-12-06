from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class Date:
    year: int

    month: Optional[int]
    day: Optional[int]

    def __post_init__(self) -> None:
        if self.year <= 0:
            msg = "Date year must be greater than 0"
            raise ValueError(msg)
        elif self.month is not None and 0 >= self.month > 12:
            msg = "Date month must be greater than 0 and less than or equal to 12"
            raise ValueError(msg)
        elif self.day is not None and 0 >= self.day > 31:
            msg = "Date day must be greater than 0 and less than or equal to 31"
            raise ValueError(msg)


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
            msg = "Money value must be greater than or equal to 0"
            raise ValueError(msg)

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
            msg = "Object must be instance of `Money`"
            raise ValueError(msg)
        elif obj.currency != self.currency:
            msg = "Money must be the same currency"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Runtime:
    minutes: int

    def __post_init__(self) -> None:
        if self.minutes <= 0:
            msg = "Runtime minutes must be greater than 0"
            raise ValueError(msg)

    def __le__(self, other: Any) -> bool:
        self._enusre_runtime(
            obj=other,
        )
        return self.minutes <= other.minutes

    def __lt__(self, other: Any) -> bool:
        self._enusre_runtime(
            obj=other,
        )
        return self.minutes < other.minutes

    def __ge__(self, other: Any) -> bool:
        self._enusre_runtime(
            obj=other,
        )
        return self.minutes >= other.minutes

    def __gt__(self, other: Any) -> bool:
        self._enusre_runtime(
            obj=other,
        )
        return self.minutes > other.minutes

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
            msg = "Object must be instance of `Runtime`"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Rating:
    value: float

    def __post_init__(self) -> None:
        if 0 >= self.value > 10 and self.value % 0.5 != 0:
            msg = "Rating must be greater than 0, less than or equal to 10 and a multiple of 0.5"
            raise ValueError(msg)
