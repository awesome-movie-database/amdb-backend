from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.queries.detailed_movie import GetDetailedMovieQuery
from amdb.application.queries.non_detailed_movies import (
    GetNonDetailedMoviesQuery,
)
from amdb.application.common.view_models.detailed_movie import (
    DetailedMovieViewModel,
)
from amdb.application.common.view_models.non_detailed_movie import (
    NonDetailedMovieViewModel,
)
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def get_non_detailed_movies(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[
        IdentityProvider,
        Depends(get_identity_provider),
    ],
    limit: int = 100,
    offset: int = 0,
) -> list[NonDetailedMovieViewModel]:
    """
    ## Errors: \n
        - When access is denied \n
    """
    with ioc.get_non_detailed_movies(
        identity_provider,
    ) as get_non_detailed_movies_handler:
        get_non_detailed_movies_query = GetNonDetailedMoviesQuery(
            limit=limit,
            offset=offset,
        )
        result = get_non_detailed_movies_handler.execute(
            get_non_detailed_movies_query,
        )
    return result


async def get_detailed_movie(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[
        IdentityProvider,
        Depends(get_identity_provider),
    ],
    movie_id: MovieId,
) -> DetailedMovieViewModel:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
    """
    with ioc.get_detailed_movie(
        identity_provider,
    ) as get_detailed_movie_handler:
        get_detailed_movie_query = GetDetailedMovieQuery(
            movie_id=movie_id,
        )
        result = get_detailed_movie_handler.execute(get_detailed_movie_query)
    return result
