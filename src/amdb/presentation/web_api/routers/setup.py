from fastapi import FastAPI

from .auth.router import create_auth_router
from .movies.router import create_movies_router
from .ratings.router import create_ratings_router
from .reviews.router import create_reviews_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(create_auth_router())
    app.include_router(create_movies_router())
    app.include_router(create_ratings_router())
    app.include_router(create_reviews_router())
