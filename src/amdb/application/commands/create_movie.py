from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class CreateMovieCommand:
    title: str
    release_date: date
