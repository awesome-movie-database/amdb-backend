from fastapi import APIRouter

from .get_my_detailed import get_my_detailed_ratings
from .rate_movie import rate_movie
from .unrate_movie import unrate_movie


ratings_router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)
ratings_router.add_api_route(
    path="/me/detailed-ratings",
    endpoint=get_my_detailed_ratings,
    methods=["GET"],
)
ratings_router.add_api_route(
    path="",
    endpoint=rate_movie,
    methods=["POST"],
)
ratings_router.add_api_route(
    path="/{rating_id}",
    endpoint=unrate_movie,
    methods=["DELETE"],
)
