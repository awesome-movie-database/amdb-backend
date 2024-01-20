from fastapi import FastAPI

from .auth.router import create_auth_router
from .ratings.router import create_ratings_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(create_auth_router())
    app.include_router(create_ratings_router())
