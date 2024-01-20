from fastapi import APIRouter

from .register import register
from .login import login


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
    router.add_api_route(
        path="/login",
        endpoint=login,
        methods=["POST"],
    )

    return router
