from dataclasses import dataclass
from datetime import timedelta
from typing import Union
from os import PathLike

import toml


@dataclass(frozen=True, slots=True)
class SessionConfig:
    lifetime: timedelta

    @classmethod
    def from_toml(cls, path: Union[PathLike, str]) -> "SessionConfig":
        toml_as_dict = toml.load(path)
        session_section_as_dict = toml_as_dict["auth-session"]
        return SessionConfig(
            lifetime=session_section_as_dict["lifetime"],
        )
