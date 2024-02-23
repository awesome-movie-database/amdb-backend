from dataclasses import dataclass

import toml


@dataclass(frozen=True, slots=True)
class WebAPIConfig:
    version: str
    host: str
    port: int

    @classmethod
    def from_toml(cls, path: str) -> "WebAPIConfig":
        toml_as_dict = toml.load(path)
        web_api_section_as_dict = toml_as_dict["web-api"]
        return WebAPIConfig(
            version=web_api_section_as_dict["version"],
            host=web_api_section_as_dict["host"],
            port=web_api_section_as_dict["port"],
        )
