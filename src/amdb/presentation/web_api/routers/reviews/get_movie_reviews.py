from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_movie_reviews import GetMovieReviewsQuery, GetMovieReviewsResult
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


async def get_movie_reviews(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    movie_id: MovieId,
    limit: int = 100,
    offset: int = 0,
) -> GetMovieReviewsResult:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
    """
    with ioc.get_movie_reviews(identity_provider) as get_movie_reviews_handler:
        get_movie_reviews_query = GetMovieReviewsQuery(
            movie_id=movie_id,
            limit=limit,
            offset=offset,
        )
        get_movie_reviews_result = get_movie_reviews_handler.execute(get_movie_reviews_query)

    return get_movie_reviews_result
