from fastapi import APIRouter

from .update_my import update_my_profile


profiles_router = APIRouter(tags=["profiles"])
profiles_router.add_api_route(
    path="/me/profile",
    endpoint=update_my_profile,
    methods=["PATCH"],
)
