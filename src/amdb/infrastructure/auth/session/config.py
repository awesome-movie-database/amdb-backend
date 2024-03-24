from dataclasses import dataclass
from datetime import timedelta

import toml


@dataclass(frozen=True, slots=True)
class SessionConfig:
    lifetime: timedelta


def load_session_config_from_toml(path: str) -> SessionConfig:
    toml_as_dict = toml.load(path)
    session_section_as_dict = toml_as_dict["auth-session"]
    return SessionConfig(
        lifetime=timedelta(minutes=session_section_as_dict["lifetime"]),
    )
