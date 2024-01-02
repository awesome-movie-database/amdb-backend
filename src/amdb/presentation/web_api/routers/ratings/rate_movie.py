from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.rate_movie import RateMovieCommand
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


class RateMovieSchema(BaseModel):
    rating: float


async def rate_movie(
    ioc: Annotated[HandlerFactory, Depends(HandlerFactory)],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
    data: RateMovieSchema,
) -> None:
    with ioc.rate_movie(identity_provider) as rate_movie_handler:
        rate_movie_command = RateMovieCommand(
            movie_id=movie_id,
            rating=data.rating,
        )
        rate_movie_handler.execute(
            command=rate_movie_command,
        )
