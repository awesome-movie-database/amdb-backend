from dataclasses import dataclass

import toml


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    url: str

    @classmethod
    def from_toml(cls, path: str) -> "PostgresConfig":
        toml_as_dict = toml.load(path)
        postgres_section_as_dict = toml_as_dict["postgres"]
        return PostgresConfig(url=postgres_section_as_dict["url"])
