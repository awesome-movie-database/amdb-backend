from fastapi import APIRouter

from .rate_movie import rate_movie
from .unrate_movie import unrate_movie


def create_ratings_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["ratings"],
    )

    router.add_api_route(
        path="/me/ratings",
        endpoint=rate_movie,
        methods=["POST"],
        tags=["me"],
    )
    router.add_api_route(
        path="/me/ratings/{rating_id}",
        endpoint=unrate_movie,
        methods=["DELETE"],
        tags=["me"],
    )

    return router
