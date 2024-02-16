from typing import Annotated

from fastapi import Depends

from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_my_ratings import (
    GetMyRatingsQuery,
    GetMyRatingsResult,
)
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def get_my_ratings(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[
        IdentityProvider, Depends(get_identity_provider)
    ],
    limit: int = 100,
    offset: int = 0,
) -> GetMyRatingsResult:
    """
    Errors: \n
        - When access is denied \n
    """
    with ioc.get_my_ratings(identity_provider) as get_my_ratings_handler:
        get_my_ratings_query = GetMyRatingsQuery(
            limit=limit,
            offset=offset,
        )
        get_my_ratings_result = get_my_ratings_handler.execute(
            get_my_ratings_query
        )

    return get_my_ratings_result
