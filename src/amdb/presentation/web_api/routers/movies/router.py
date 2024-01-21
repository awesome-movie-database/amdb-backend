from fastapi import APIRouter

from .get_movie import get_movie


def create_movies_router() -> APIRouter:
    router = APIRouter(
        prefix="/movies",
        tags=["movies"],
    )

    router.add_api_route(
        path="/{movie_id}",
        endpoint=get_movie,
        methods=["GET"],
    )

    return router
