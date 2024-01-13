from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    host: str
    port: str
    name: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name,
        )
