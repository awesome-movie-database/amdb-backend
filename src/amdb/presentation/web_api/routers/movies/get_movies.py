from typing import Annotated

from fastapi import Depends

from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider
from amdb.application.queries.get_movies import GetMoviesQuery, GetMoviesResult


async def get_movies(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    limit: int = 100,
    offset: int = 0,
) -> GetMoviesResult:
    """
    ## Errors: \n
        - When access is denied \n
    """
    with ioc.get_movies(identity_provider) as get_movies_handler:
        get_movies_query = GetMoviesQuery(
            limit=limit,
            offset=offset,
        )
        get_movies_result = get_movies_handler.execute(get_movies_query)

    return get_movies_result
