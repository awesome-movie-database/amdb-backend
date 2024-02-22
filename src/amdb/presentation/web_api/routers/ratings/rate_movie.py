from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.rating import RatingId
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.rate_movie import RateMovieCommand
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def rate_movie(
    ioc: Annotated[HandlerFactory, Depends(HandlerFactory)],
    identity_provider: Annotated[
        IdentityProvider,
        Depends(get_identity_provider),
    ],
    rate_movie_command: RateMovieCommand,
) -> RatingId:
    """
    ## Returns: \n
        - Rating id
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
        - When movie is already rated \n
    """
    with ioc.rate_movie(identity_provider) as rate_movie_handler:
        rating_id = rate_movie_handler.execute(rate_movie_command)

    return rating_id
