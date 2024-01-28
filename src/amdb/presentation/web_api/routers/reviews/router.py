from fastapi import APIRouter

from .get_movie_reviews import get_movie_reviews
from .review_movie import review_movie
from .get_review import get_review


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
        path="/reviews/{review_id}",
        endpoint=get_review,
        methods=["GET"],
    )
    router.add_api_route(
        path="/me/reviews",
        endpoint=review_movie,
        methods=["POST"],
        tags=["me"],
    )
    router.add_api_route(
        path="/me/reviews/{review_id}",
        endpoint=get_review,
        methods=["GET"],
        tags=["me"],
    )

    return router
