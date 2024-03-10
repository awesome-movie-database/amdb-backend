from fastapi import APIRouter

from .get_non_detailed import get_non_detailed_movies
from .get_detailed import get_detailed_movie


movies_router = APIRouter(tags=["movies"])
movies_router.add_api_route(
    path="/non-detailed-movies",
    endpoint=get_non_detailed_movies,
    methods=["GET"],
)
movies_router.add_api_route(
    path="/detailed-movies/{movie_id}",
    endpoint=get_detailed_movie,
    methods=["GET"],
)
