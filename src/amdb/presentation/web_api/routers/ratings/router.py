from fastapi import APIRouter

from .get_rating import get_movie_rating
from .rate_movie import rate_movie
from .unrate_movie import unrate_movie


def create_ratings_router() -> APIRouter:
    router = APIRouter(
        prefix="/me/ratings",
        tags=["ratings"],
    )

    router.add_api_route(
        path="/{movie_id}",
        endpoint=get_movie_rating,
        methods=["GET"],
    )
    router.add_api_route(
        path="/{movie_id}",
        endpoint=rate_movie,
        methods=["POST"],
    )
    router.add_api_route(
        path="/{movie_id}",
        endpoint=unrate_movie,
        methods=["DELETE"],
    )

    return router
