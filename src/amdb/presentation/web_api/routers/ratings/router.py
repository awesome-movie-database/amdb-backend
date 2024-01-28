from fastapi import APIRouter

from .get_movie_ratings import get_movie_ratings
from .get_rating import get_rating
from .rate_movie import rate_movie
from .unrate_movie import unrate_movie


def create_ratings_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["ratings"],
    )

    router.add_api_route(
        path="/movies/{movie_id}/ratings",
        endpoint=get_movie_ratings,
        methods=["GET"],
        tags=["movies"],
    )
    router.add_api_route(
        path="/ratings/{rating_id}",
        endpoint=get_rating,
        methods=["GET"],
    )
    router.add_api_route(
        path="/me/ratings",
        endpoint=rate_movie,
        methods=["POST"],
        tags=["me"],
    )
    router.add_api_route(
        path="/me/ratings/{rating_id}",
        endpoint=get_rating,
        methods=["GET"],
        tags=["me"],
    )
    router.add_api_route(
        path="/me/ratings/{rating_id}",
        endpoint=unrate_movie,
        methods=["DELETE"],
        tags=["me"],
    )

    return router
