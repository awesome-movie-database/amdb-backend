from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.unrate_movie import UnrateMovieCommand
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


async def unrate_movie(
    ioc: Annotated[HandlerFactory, Depends(HandlerFactory)],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
) -> None:
    with ioc.unrate_movie(identity_provider) as unrate_movie_handler:
        unrate_movie_command = UnrateMovieCommand(
            movie_id=movie_id,
        )
        unrate_movie_handler.execute(
            command=unrate_movie_command,
        )
