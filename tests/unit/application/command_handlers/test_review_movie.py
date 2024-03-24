from unittest.mock import Mock
from datetime import date, datetime, timezone

import pytest
from uuid_extensions import uuid7

from amdb.domain.entities.user import UserId, User
from amdb.domain.entities.movie import MovieId, Movie
from amdb.domain.entities.review import ReviewId, ReviewType, Review
from amdb.domain.services.access_concern import AccessConcern
from amdb.domain.services.review_movie import ReviewMovie
from amdb.domain.constants.exceptions import (
    INVALID_REVIEW_TITLE,
    INVALID_REVIEW_CONTENT,
)
from amdb.domain.exception import DomainError
from amdb.application.common.gateways.permissions import PermissionsGateway
from amdb.application.common.gateways.user import UserGateway
from amdb.application.common.gateways.movie import MovieGateway
from amdb.application.common.gateways.review import ReviewGateway
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.identity_provider import IdentityProvider
from amdb.application.commands.review_movie import ReviewMovieCommand
from amdb.application.command_handlers.review_movie import ReviewMovieHandler
from amdb.application.common.constants.exceptions import (
    REVIEW_MOVIE_ACCESS_DENIED,
    MOVIE_DOES_NOT_EXIST,
    MOVIE_ALREADY_REVIEWED,
)
from amdb.application.common.exception import ApplicationError


@pytest.fixture
def identity_provider_with_correct_permissions(
    permissions_gateway: PermissionsGateway,
) -> IdentityProvider:
    identity_provider = Mock()

    correct_permissions = permissions_gateway.for_review_movie()
    identity_provider.permissions = Mock(return_value=correct_permissions)

    return identity_provider


def test_review_movie(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
        telegram=None,
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Matrix",
        release_date=date(1999, 3, 31),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.user_id = Mock(
        return_value=user.id,
    )

    command = ReviewMovieCommand(
        movie_id=movie.id,
        title="Not bad",
        content="Great soundtrack",
        type=ReviewType.POSITIVE,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    handler.execute(command)


def test_review_movie_should_raise_error_when_access_is_denied(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_incorrect_permissions: IdentityProvider,
):
    command = ReviewMovieCommand(
        movie_id=MovieId(uuid7()),
        title="Mid",
        content="So-so..",
        type=ReviewType.NEUTRAL,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_incorrect_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == REVIEW_MOVIE_ACCESS_DENIED


def test_review_movie_should_raise_error_when_movie_does_not_exist(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    command = ReviewMovieCommand(
        movie_id=MovieId(uuid7()),
        title="Fantastic",
        content="Awesome!!",
        type=ReviewType.POSITIVE,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_DOES_NOT_EXIST


def test_review_movie_should_raise_error_when_movie_already_reviewed(
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
        telegram=None,
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Gone girl",
        release_date=date(2014, 10, 3),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    review = Review(
        id=ReviewId(uuid7()),
        user_id=user.id,
        movie_id=movie.id,
        title="Masterpice",
        content="Extremely underrated",
        type=ReviewType.POSITIVE,
        created_at=datetime.now(timezone.utc),
    )
    review_gateway.save(review)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.user_id = Mock(
        return_value=user.id,
    )

    command = ReviewMovieCommand(
        movie_id=movie.id,
        title="Masterpice",
        content="Extremely underrated",
        type=ReviewType.POSITIVE,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(ApplicationError) as error:
        handler.execute(command)

    assert error.value.message == MOVIE_ALREADY_REVIEWED


REVIEW_TITLE_SHORTER_THAN_5_CHARACTERS = "Bad!"
REVIEW_TITLE_LONGER_THAN_128_CHARACTERS = "_" * 129


@pytest.mark.parametrize(
    "review_title",
    (
        REVIEW_TITLE_SHORTER_THAN_5_CHARACTERS,
        REVIEW_TITLE_LONGER_THAN_128_CHARACTERS,
    ),
)
def test_review_movie_should_raise_error_when_title_is_invalid(
    review_title: str,
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
        telegram=None,
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Gone girl",
        release_date=date(2014, 10, 3),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.user_id = Mock(
        return_value=user.id,
    )

    command = ReviewMovieCommand(
        movie_id=movie.id,
        title=review_title,
        content="Extremely underrated",
        type=ReviewType.POSITIVE,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_REVIEW_TITLE


REVIEW_CONTENT_SHORTER_THAN_5_CHARACTERS = "Bad!"
REVIEW_CONTENT_LONGER_THAN_1024_CHARACTERS = "_" * 1025


@pytest.mark.parametrize(
    "review_content",
    (
        REVIEW_CONTENT_SHORTER_THAN_5_CHARACTERS,
        REVIEW_CONTENT_LONGER_THAN_1024_CHARACTERS,
    ),
)
def test_review_movie_should_raise_error_when_content_is_invalid(
    review_content: str,
    permissions_gateway: PermissionsGateway,
    movie_gateway: MovieGateway,
    user_gateway: UserGateway,
    review_gateway: ReviewGateway,
    unit_of_work: UnitOfWork,
    identity_provider_with_correct_permissions: IdentityProvider,
):
    user = User(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="John@doe.com",
        telegram=None,
    )
    user_gateway.save(user)

    movie = Movie(
        id=MovieId(uuid7()),
        title="Gone girl",
        release_date=date(2014, 10, 3),
        rating=0,
        rating_count=0,
    )
    movie_gateway.save(movie)

    unit_of_work.commit()

    identity_provider_with_correct_permissions.user_id = Mock(
        return_value=user.id,
    )

    command = ReviewMovieCommand(
        movie_id=movie.id,
        title="Bad!!!!",
        content=review_content,
        type=ReviewType.POSITIVE,
    )
    handler = ReviewMovieHandler(
        access_concern=AccessConcern(),
        review_movie=ReviewMovie(),
        permissions_gateway=permissions_gateway,
        user_gateway=user_gateway,
        movie_gateway=movie_gateway,
        review_gateway=review_gateway,
        unit_of_work=unit_of_work,
        identity_provider=identity_provider_with_correct_permissions,
    )

    with pytest.raises(DomainError) as error:
        handler.execute(command)

    assert error.value.message == INVALID_REVIEW_CONTENT
