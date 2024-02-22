import asyncio
import os

from uvicorn import Server, Config

from amdb.infrastructure.persistence.sqlalchemy.config import PostgresConfig
from amdb.infrastructure.persistence.redis.config import RedisConfig
from amdb.infrastructure.auth.session.config import SessionConfig
from .config import WebAPIConfig
from .app import create_app


async def main() -> None:
    path_to_config = os.getenv("CONFIG_PATH")
    if not path_to_config:
        message = "Path to config env var is not set"
        raise ValueError(message)

    web_api_config = WebAPIConfig.from_toml(path_to_config)
    postgres_config = PostgresConfig.from_toml(path_to_config)
    redis_config = RedisConfig.from_toml(path_to_config)
    session_config = SessionConfig.from_toml(path_to_config)

    app = create_app(
        web_api_config=web_api_config,
        postgres_config=postgres_config,
        redis_config=redis_config,
        session_config=session_config,
    )
    server = Server(
        Config(
            app=app,
            host=web_api_config.host,
            port=web_api_config.port,
        ),
    )

    await server.serve()


asyncio.run(main())
