from fastapi import APIRouter

from .get_movie_reviews import get_movie_reviews
from .review_movie import review_movie


def create_reviews_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["reviews"],
    )

    router.add_api_route(
        path="/movies/{movie_id}/reviews",
        endpoint=get_movie_reviews,
        methods=["GET"],
        tags=["movies"],
    )
    router.add_api_route(
        path="/movies/{movie_id}/reviews",
        endpoint=review_movie,
        methods=["POST"],
        tags=["movies"],
    )

    return router
