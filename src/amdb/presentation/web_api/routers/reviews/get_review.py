from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.review import ReviewId
from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.queries.get_review import GetReviewQuery, GetReviewResult
from amdb.presentation.handler_factory import HandlerFactory
from amdb.presentation.web_api.dependencies.identity_provider import get_identity_provider


async def get_review(
    ioc: Annotated[HandlerFactory, Depends()],
    identity_provider: Annotated[IdentityProvider, Depends(get_identity_provider)],
    review_id: ReviewId,
) -> GetReviewResult:
    """
    ## Errors: \n
        - When access is denied \n
        - When review doesn't exist \n
    """
    with ioc.get_review(identity_provider) as get_review_handler:
        get_review_query = GetReviewQuery(
            review_id=review_id,
        )
        get_review_result = get_review_handler.execute(get_review_query)

    return get_review_result
