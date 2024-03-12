from fastapi import APIRouter

from .add_movie import add_movie_to_watchlist
from .delete_movie import delete_movie_from_watchlist


watchlists_router = APIRouter(tags=["watchlists"])
watchlists_router.add_api_route(
    path="/my/movies-for-later",
    endpoint=add_movie_to_watchlist,
    methods=["POST"],
)
watchlists_router.add_api_route(
    path="/my/movies-for-later/{movie_for_later_id}",
    endpoint=delete_movie_from_watchlist,
    methods=["DELETE"],
)
