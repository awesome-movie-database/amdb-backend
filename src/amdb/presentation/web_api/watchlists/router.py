from fastapi import APIRouter

from .get_my_detailed import get_my_detailed_watchlist
from .add_movie import add_movie_to_watchlist
from .delete_movie import delete_movie_from_watchlist


watchlists_router = APIRouter(tags=["watchlists"])
watchlists_router.add_api_route(
    path="/me/detailed-movies-for-later",
    endpoint=get_my_detailed_watchlist,
    methods=["GET"],
)
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
