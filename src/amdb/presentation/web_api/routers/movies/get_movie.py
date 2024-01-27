from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movie import GetMovieResult, GetMovieQuery
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


def get_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
) -> GetMovieResult:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
    """
    with ioc.get_movie(identity_provider) as get_movie_handler:
        get_movie_query = GetMovieQuery(
            movie_id=movie_id,
        )
        get_movie_result = get_movie_handler.execute(get_movie_query)

    return get_movie_result
