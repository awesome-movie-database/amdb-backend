import asyncio

from uvicorn import Server, Config

from amdb.main.config import build_generic_config
from .config import build_web_api_config
from .app import create_app


async def main() -> None:
    web_api_config = build_web_api_config()
    generic_config = build_generic_config()

    app = create_app(
        fastapi_config=web_api_config.fastapi,
        session_config=web_api_config.session,
        generic_config=generic_config,
    )
    server = Server(
        Config(
            app=app,
            host=web_api_config.uvicorn.host,
            port=web_api_config.uvicorn.port,
        ),
    )

    await server.serve()


asyncio.run(main())
