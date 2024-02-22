from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.rating import RatingId
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.unrate_movie import UnrateMovieCommand
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def unrate_movie(
    ioc: Annotated[HandlerFactory, Depends(HandlerFactory)],
    identity_provider: Annotated[
        IdentityProvider,
        Depends(get_identity_provider),
    ],
    rating_id: RatingId,
) -> None:
    """
    ## Errors: \n
        - When access is denied \n
        - When user is not an owner of rating \n
        - When movie is already rated \n
    """
    with ioc.unrate_movie(identity_provider) as unrate_movie_handler:
        unrate_movie_command = UnrateMovieCommand(
            rating_id=rating_id,
        )
        unrate_movie_handler.execute(unrate_movie_command)
