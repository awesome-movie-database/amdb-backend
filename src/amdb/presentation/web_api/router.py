from fastapi import APIRouter

from .auth.router import auth_router
from .movies.router import movies_router
from .ratings.router import ratings_router
from .reviews.router import reviews_router


router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(movies_router)
router.include_router(ratings_router)
router.include_router(reviews_router)
