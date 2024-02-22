from fastapi import APIRouter

from .get_reviews import get_reviews
from .review_movie import review_movie


def create_reviews_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["reviews"],
    )

    router.add_api_route(
        path="/movies/{movie_id}/reviews",
        endpoint=get_reviews,
        methods=["GET"],
    )
    router.add_api_route(
        path="/me/reviews",
        endpoint=review_movie,
        methods=["POST"],
        tags=["me"],
    )

    return router
