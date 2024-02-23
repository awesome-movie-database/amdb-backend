from fastapi import APIRouter

from .get_detailed import get_detailed_reviews
from .review_movie import review_movie


reviews_router = APIRouter(tags=["reviews"])
reviews_router.add_api_route(
    path="/movies/{movie_id}/detailed-reviews",
    endpoint=get_detailed_reviews,
    methods=["GET"],
)
reviews_router.add_api_route(
    path="/reviews",
    endpoint=review_movie,
    methods=["POST"],
)
