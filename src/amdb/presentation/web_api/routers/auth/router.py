from fastapi import APIRouter

from .register import register


def create_auth_router() -> APIRouter:
    router = APIRouter(
        prefix="/auth",
        tags=["auth"],
    )

    router.add_api_route(
        path="/register",
        endpoint=register,
        methods=["POST"],
    )

    return router
