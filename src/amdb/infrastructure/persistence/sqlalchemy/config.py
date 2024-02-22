from dataclasses import dataclass
from typing import Union
from os import PathLike

import toml


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    url: str

    @classmethod
    def from_toml(cls, path: Union[PathLike, str]) -> "PostgresConfig":
        toml_as_dict = toml.load(path)
        postgres_section_as_dict = toml_as_dict["postgres"]
        return PostgresConfig(url=postgres_section_as_dict["url"])
