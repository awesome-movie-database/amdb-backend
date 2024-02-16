from typing import Annotated

from fastapi import Depends

from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_my_reviews import (
    GetMyReviewsQuery,
    GetMyReviewsResult,
)
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def get_my_reviews(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[
        IdentityProvider, Depends(get_identity_provider)
    ],
    limit: int = 100,
    offset: int = 0,
) -> GetMyReviewsResult:
    with ioc.get_my_reviews(identity_provider) as get_my_reviews_handler:
        get_my_reviews_query = GetMyReviewsQuery(
            limit=limit,
            offset=offset,
        )
        get_my_reviews_result = get_my_reviews_handler.execute(
            get_my_reviews_query
        )

    return get_my_reviews_result
