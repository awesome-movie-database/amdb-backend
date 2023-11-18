from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:

    value: int
    currency: str
