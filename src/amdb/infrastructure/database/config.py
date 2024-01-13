import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    pg_host: str
    pg_port: str
    pg_name: str
    pg_user: str
    pg_password: str

    @property
    def pg_dsn(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.pg_user,
            self.pg_password,
            self.pg_host,
            self.pg_port,
            self.pg_name,
        )

    @property
    def alembic_config_path(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.abspath())
        )
