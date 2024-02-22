from typing import Annotated

from fastapi import Depends

from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.review import ReviewViewModel
from amdb.application.queries.reviews import GetReviewsQuery
from amdb.presentation.handler_factory import HandlerFactory


async def get_reviews(
    ioc: Annotated[HandlerFactory, Depends()],
    movie_id: MovieId,
    limit: int = 100,
    offset: int = 0,
) -> list[ReviewViewModel]:
    """
    ## Errors: \n
        - When movie doesn't exist \n
    """
    with ioc.get_reviews() as get_reviews_handler:
        get_reviews_query = GetReviewsQuery(
            movie_id=movie_id,
            limit=limit,
            offset=offset,
        )
        result = get_reviews_handler.execute(get_reviews_query)
    return result
