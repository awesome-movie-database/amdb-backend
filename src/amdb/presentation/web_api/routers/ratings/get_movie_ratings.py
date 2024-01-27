from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movie_ratings import GetMovieRatingsQuery, GetMovieRatingsResult
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


async def get_movie_ratings(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
    limit: int = 100,
    offset: int = 0,
) -> GetMovieRatingsResult:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
    """
    with ioc.get_movie_ratings(identity_provider) as get_movie_ratings_handler:
        get_movie_ratings_query = GetMovieRatingsQuery(
            movie_id=movie_id,
            limit=limit,
            offset=offset,
        )
        get_movie_ratings_result = get_movie_ratings_handler.execute(get_movie_ratings_query)

    return get_movie_ratings_result
