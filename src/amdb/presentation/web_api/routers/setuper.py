from fastapi import FastAPI

from .ratings.router import create_ratings_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(create_ratings_router())
