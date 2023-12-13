import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.entities.user.user import UserId, User
from amdb.domain.entities.user.profile import Profile
from amdb.domain.services.user.create_user import CreateUser
from amdb.domain.services.user.create_profile import CreateProfile
from amdb.application.common.interfaces.gateways.user.user import UserGateway
from amdb.application.common.interfaces.gateways.user.profile import ProfileGateway
from amdb.application.common.interfaces.unit_of_work import UnitOfWork
from amdb.application.common.constants.exceptions import USER_NAME_ALREADY_EXISTS
from amdb.application.common.exception import ApplicationError
from amdb.application.commands.user.register_user import RegisterUserCommand
from amdb.application.command_handlers.user.register_user import RegisterUserHandler


USER_ID = UserId(uuid4())
USER_NAME = "JohnDoe"
USER_PASSWORD = "password"
USER_IS_ACTIVE = True
USER_IS_VERIFIED = False
USER_CREATED_AT = datetime.now(timezone.utc)
USER_EMAIL = None
USER_SEX = None
USER_BIRTH_DATE = None
USER_LOCATION = None
USER_VERIFIED_AT = None
USER_UPDATED_AT = None

PROFILE_ACHIEVEMENTS = 0
PROFILE_MOVIE_RATINGS = 0
PROFILE_SERIES_EPISODE_RATINGS = 0
PROFILE_APPROVED_REVIEWS = 0
PROFILE_MOVIE_REVIEWS = 0
PROFILE_SERIES_REVIEWS = 0
PROFILE_SERIES_SEASON_REVIEWS = 0
PROFILE_SERIES_EPISODE_REVIEWS = 0
PROFILE_GIVEN_VOTES = 0
PROFILE_GAINED_VOTES = 0


def test_register_user(
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    user = User(
        id=USER_ID,
        name=USER_NAME,
        password=USER_PASSWORD,
        is_active=USER_IS_ACTIVE,
        is_verified=USER_IS_VERIFIED,
        created_at=USER_CREATED_AT,
        email=USER_EMAIL,
        sex=USER_SEX,
        birth_date=USER_BIRTH_DATE,
        location=USER_LOCATION,
        verified_at=USER_VERIFIED_AT,
        updated_at=USER_UPDATED_AT,
    )
    create_user: CreateUser = Mock(
        return_value=user,
    )
    profile = Profile(
        user_id=USER_ID,
        achievements=PROFILE_ACHIEVEMENTS,
        movie_ratings=PROFILE_MOVIE_RATINGS,
        series_episode_ratings=PROFILE_SERIES_EPISODE_RATINGS,
        approved_reviews=PROFILE_APPROVED_REVIEWS,
        movie_reviews=PROFILE_MOVIE_REVIEWS,
        series_reviews=PROFILE_SERIES_REVIEWS,
        series_season_reviews=PROFILE_SERIES_SEASON_REVIEWS,
        series_episode_reviews=PROFILE_SERIES_EPISODE_REVIEWS,
        given_votes=PROFILE_GIVEN_VOTES,
        gained_votes=PROFILE_GAINED_VOTES,
    )
    create_profile: CreateProfile = Mock(
        return_value=profile,
    )
    user_gateway.check_exists_with_name = Mock(
        return_value=False,
    )

    register_user_command = RegisterUserCommand(
        name=USER_NAME,
        password=USER_PASSWORD,
    )
    register_user_handler = RegisterUserHandler(
        create_user=create_user,
        create_profile=create_profile,
        user_gateway=user_gateway,
        profile_gateway=profile_gateway,
        unit_of_work=unit_of_work,
    )
    user_id = register_user_handler.execute(
        command=register_user_command,
    )

    assert user_id == USER_ID


def test_register_user_raises_error_when_username_already_exists(
    user_gateway: UserGateway,
    profile_gateway: ProfileGateway,
    unit_of_work: UnitOfWork,
) -> None:
    create_user: CreateUser = Mock()
    create_profile: CreateProfile = Mock()
    user_gateway.check_exists_with_name = Mock(
        return_value=True,
    )

    register_user_command = RegisterUserCommand(
        name=USER_NAME,
        password=USER_PASSWORD,
    )
    register_user_handler = RegisterUserHandler(
        create_user=create_user,
        create_profile=create_profile,
        user_gateway=user_gateway,
        profile_gateway=profile_gateway,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ApplicationError) as error:
        register_user_handler.execute(
            command=register_user_command,
        )
    assert error.value.messsage == USER_NAME_ALREADY_EXISTS
