from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.detailed_review import (
    DetailedReviewViewModel,
)
from amdb.application.queries.detailed_reviews import GetDetailedReviewsQuery
from amdb.application.query_handlers.detailed_reviews import (
    GetDetailedReviewsHandler,
)


@inject
async def get_detailed_reviews(
    *,
    handler: Annotated[GetDetailedReviewsHandler, FromDishka()],
    movie_id: MovieId,
    limit: int = 100,
    offset: int = 0,
) -> list[DetailedReviewViewModel]:
    """
    Returns detailed movie reviews with ratings.\n\n

    #### Returns 400:
        * When movie doesn't exist
    """
    query = GetDetailedReviewsQuery(
        movie_id=movie_id,
        limit=limit,
        offset=offset,
    )

    return handler.execute(query)
