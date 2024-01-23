from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePersonCommand:
    name: str
