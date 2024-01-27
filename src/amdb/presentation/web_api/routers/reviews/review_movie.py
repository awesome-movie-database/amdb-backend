from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from amdb.domain.entities.movie import MovieId
from amdb.domain.entities.review import ReviewId, ReviewType
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.review_movie import ReviewMovieCommand
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


class ReviewMovieSchema(BaseModel):
    title: str
    content: str
    type: ReviewType


async def review_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
    data: ReviewMovieSchema,
) -> ReviewId:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
        - When movie is already reviewd \n
    """
    with ioc.review_movie(identity_provider) as review_movie_handler:
        review_movie_command = ReviewMovieCommand(
            movie_id=movie_id,
            title=data.title,
            content=data.content,
            type=data.type,
        )
        review_id = review_movie_handler.execute(review_movie_command)

    return review_id
