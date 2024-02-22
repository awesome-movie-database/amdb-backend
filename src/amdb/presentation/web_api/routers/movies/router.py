from fastapi import APIRouter

from .get_movies import get_non_detailed_movies, get_detailed_movie


def create_movies_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["movies"],
    )

    router.add_api_route(
        path="/non-detailed-movies",
        endpoint=get_non_detailed_movies,
        methods=["GET"],
    )
    router.add_api_route(
        path="/detailed-movies/{movie_id}",
        endpoint=get_detailed_movie,
        methods=["GET"],
    )

    return router
