from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.rating import RatingId
from amdb.application.common.interfaces.identity_provider import (
    IdentityProvider,
)
from amdb.application.queries.get_rating import GetRatingQuery, GetRatingResult
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import (
    get_identity_provider,
)


async def get_rating(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[
        IdentityProvider, Depends(get_identity_provider)
    ],
    rating_id: RatingId,
) -> GetRatingResult:
    """
    ## Errors: \n
        - When access is denied \n
        - When movie doesn't exist \n
        - When rating doesn't exist \n
    """
    with ioc.get_rating(identity_provider) as get_rating_handler:
        get_rating_query = GetRatingQuery(
            rating_id=rating_id,
        )
        get_rating_result = get_rating_handler.execute(get_rating_query)

    return get_rating_result
