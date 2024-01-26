from fastapi import APIRouter

from .review_movie import review_movie


def create_reviews_router() -> APIRouter:
    router = APIRouter(
        prefix="",
        tags=["reviews"],
    )

    router.add_api_route(
        path="/movies/{movie_id}/reviews",
        endpoint=review_movie,
        methods=["POST"],
        tags=["movies"],
    )

    return router
