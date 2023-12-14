import pytest
from datetime import datetime, timezone
from uuid import uuid4

from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.create_user import CreateUser
from amdb.domain.services.user.update_user import UpdateUser
from amdb.domain.services.user.verify_user import VerifyUser
from amdb.domain.services.user.create_profile import CreateProfile
from amdb.domain.entities.user.user import UserId, User
from amdb.domain.entities.user.profile import Profile


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


@pytest.fixture
def user() -> User:
    return User(
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


@pytest.fixture(scope="session")
def access_concern() -> AccessConcern:
    return AccessConcern()


@pytest.fixture(scope="session")
def create_user() -> CreateUser:
    return CreateUser()


@pytest.fixture(scope="session")
def update_user() -> UpdateUser:
    return UpdateUser()


@pytest.fixture(scope="session")
def verify_user() -> VerifyUser:
    return VerifyUser()


@pytest.fixture
def profile() -> Profile:
    return Profile(
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


@pytest.fixture(scope="session")
def create_profile() -> CreateProfile:
    return CreateProfile()
