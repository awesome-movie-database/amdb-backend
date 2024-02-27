from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .my_ratings import export_my_ratings


exports_router = APIRouter(
    prefix="/exports",
    tags=["exports"],
)
exports_router.add_api_route(
    path="/my-ratings",
    endpoint=export_my_ratings,
    methods=["GET"],
    response_class=StreamingResponse,
)
