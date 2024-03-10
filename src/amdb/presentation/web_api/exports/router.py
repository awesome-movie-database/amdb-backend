from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .my_ratings import export_my_ratings
from .request_my_ratings import request_my_ratings_export


exports_router = APIRouter(
    prefix="",
    tags=["exports"],
)
exports_router.add_api_route(
    path="/my-ratings-export",
    endpoint=export_my_ratings,
    methods=["GET"],
    response_class=StreamingResponse,
)
exports_router.add_api_route(
    path="/my-ratings-export-requests",
    endpoint=request_my_ratings_export,
    methods=["POST"],
)
