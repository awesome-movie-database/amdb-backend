from fastapi import APIRouter

from .add_movie import add_movie_to_watchlist


watchlists_router = APIRouter(tags=["watchlists"])
watchlists_router.add_api_route(
    path="/my/watchlist/movies",
    endpoint=add_movie_to_watchlist,
    methods=["POST"],
)
