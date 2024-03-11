from fastapi import APIRouter

from .register import register
from .login import login
from .logout import logout


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
auth_router.add_api_route(
    path="/register",
    endpoint=register,
    methods=["POST"],
)
auth_router.add_api_route(
    path="/login",
    endpoint=login,
    methods=["POST"],
)
auth_router.add_api_route(
    path="/logout",
    endpoint=logout,
    methods=["DELETE"],
)
