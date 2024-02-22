from dataclasses import dataclass
from typing import Union
from os import PathLike

import toml


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str

    @classmethod
    def from_toml(cls, path: Union[PathLike, str]) -> "RedisConfig":
        toml_as_dict = toml.load(path)
        redis_section_as_dict = toml_as_dict["redis"]
        return RedisConfig(url=redis_section_as_dict["url"])
