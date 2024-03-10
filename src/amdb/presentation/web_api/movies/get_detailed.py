from typing import Annotated, Optional

from fastapi import Cookie
from dishka.integrations.fastapi import FromDishka, inject

from amdb.domain.entities.movie import MovieId
from amdb.application.common.view_models.detailed_movie import (
    DetailedMovieViewModel,
)
from amdb.application.queries.detailed_movie import GetDetailedMovieQuery
from amdb.application.query_handlers.detailed_movie import (
    GetDetailedMovieHandler,
)
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.infrastructure.auth.session.session import SessionId
from amdb.infrastructure.auth.session.session_gateway import SessionGateway
from amdb.infrastructure.auth.session.identity_provider import (
    SessionIdentityProvider,
)
from amdb.presentation.create_handler import CreateHandler
from amdb.presentation.web_api.constants import SESSION_ID_COOKIE


HandlerMaker = CreateHandler[GetDetailedMovieHandler]


@inject
async def get_detailed_movie(
    *,
    create_handler: Annotated[HandlerMaker, FromDishka()],
    session_gateway: Annotated[SessionGateway, FromDishka()],
    permissions_gateway: Annotated[PermissionsGateway, FromDishka()],
    session_id: Annotated[
        Optional[str],
        Cookie(alias=SESSION_ID_COOKIE),
    ] = None,
    movie_id: MovieId,
) -> DetailedMovieViewModel:
    """
    Returns detailed movie information, detailed current user rating
    and review on it. \n\n

    #### Returns 400:
        * When movie doesn't exist
    """
    identity_provider = SessionIdentityProvider(
        session_id=SessionId(session_id) if session_id else None,
        session_gateway=session_gateway,
        permissions_gateway=permissions_gateway,
    )

    handler = create_handler(identity_provider)
    query = GetDetailedMovieQuery(movie_id=movie_id)

    return handler.execute(query)
