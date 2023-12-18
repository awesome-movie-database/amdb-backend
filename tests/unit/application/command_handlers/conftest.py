from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from amdb.domain.entities.user.user import UserId, User
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.person.person import PersonId, Person
from amdb.domain.entities.person.marriage import MarriageId, MarriageStatus, Marriage
from amdb.domain.constants.common import Sex
from amdb.domain.value_objects import Date, Place
from amdb.domain.services.user.access_concern import AccessConcern
from amdb.domain.services.user.create_user import CreateUser
from amdb.domain.services.user.update_user import UpdateUser
from amdb.domain.services.user.verify_user import VerifyUser
from amdb.domain.services.user.create_profile import CreateProfile
from amdb.domain.services.person.create_person import CreatePerson
from amdb.domain.services.person.update_person import UpdatePerson
from amdb.domain.services.person.create_marriage import CreateMarriage
from amdb.domain.services.person.update_marriage import UpdateMarriage
from amdb.domain.services.person.create_relation import CreateRelation


USER_ID = UserId(uuid4())
USER_NAME = "JohnDoe"
USER_PASSWORD = "password"
USER_IS_ACTIVE = True
USER_IS_VERIFIED = False
USER_CREATED_AT = datetime.now(timezone.utc)
USER_EMAIL = "john@doe.com"
USER_SEX = Sex.MALE
USER_BIRTH_DATE = date(year=1999, month=10, day=30)
USER_LOCATION = Place(country="Germany", state=None, city="Berlin")
USER_VERIFIED_AT = datetime.now(timezone.utc)
USER_UPDATED_AT = datetime.now(timezone.utc)

OTHER_USER_ID = UserId(uuid4())
OTHER_USER_NAME = "JaneDoe"
OTHER_USER_PASSWORD = "password"
OTHER_USER_IS_ACTIVE = True
OTHER_USER_IS_VERIFIED = False
OTHER_USER_CREATED_AT = datetime.now(timezone.utc)
OTHER_USER_EMAIL = "jane@doe.com"
OTHER_USER_SEX = Sex.FEMALE
OTHER_USER_BIRTH_DATE = date(year=2000, month=7, day=2)
OTHER_USER_LOCATION = Place(country="France", state=None, city="Paris")
OTHER_USER_VERIFIED_AT = datetime.now(timezone.utc)
OTHER_USER_UPDATED_AT = datetime.now(timezone.utc)

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

OTHER_PROFILE_ACHIEVEMENTS = 0
OTHER_PROFILE_MOVIE_RATINGS = 0
OTHER_PROFILE_SERIES_EPISODE_RATINGS = 0
OTHER_PROFILE_APPROVED_REVIEWS = 0
OTHER_PROFILE_MOVIE_REVIEWS = 0
OTHER_PROFILE_SERIES_REVIEWS = 0
OTHER_PROFILE_SERIES_SEASON_REVIEWS = 0
OTHER_PROFILE_SERIES_EPISODE_REVIEWS = 0
OTHER_PROFILE_GIVEN_VOTES = 0
OTHER_PROFILE_GAINED_VOTES = 0

PERSON_ID = PersonId(uuid4())
PERSON_NAME = "John Doe"
PERSON_SEX = Sex.MALE
PERSON_CREATED_AT = datetime.now(timezone.utc)
PERSON_BIRTH_DATE = Date(year=1920, month=None, day=None)
PERSON_BIRTH_PLACE = Place(country="USA", state="Texas", city=None)
PERSON_DEATH_DATE = Date(year=2004, month=1, day=7)
PERSON_DEATH_PLACE = Place(country="USA", state="Oklahoma", city=None)
PERSON_UPDATED_AT = datetime.now(timezone.utc)

OTHER_PERSON_ID = PersonId(uuid4())
OTHER_PERSON_NAME = "Jane Doe"
OTHER_PERSON_SEX = Sex.FEMALE
OTHER_PERSON_CREATED_AT = datetime.now(timezone.utc)
OTHER_PERSON_BIRTH_DATE = Date(year=1935, month=3, day=5)
OTHER_PERSON_BIRTH_PLACE = Place(country="USA", state="Oklahoma", city=None)
OTHER_PERSON_DEATH_DATE = Date(year=2014, month=10, day=14)
OTHER_PERSON_DEATH_PLACE = Place(country="USA", state="Texas", city=None)
OTHER_PERSON_UPDATED_AT = datetime.now(timezone.utc)

MARRIAGE_ID = MarriageId(uuid4())
MARRIAGE_HUSBAND_ID = PERSON_ID
MARRIAGE_WIFE_ID = OTHER_PERSON_ID
MARRIAGE_CHILD_IDS: list[PersonId] = []
MARRIAGE_STATUS = MarriageStatus.MARRIAGE
MARRIAGE_START_DATE = Date(year=2010, month=12, day=31)
MARRIAGE_END_DATE = None


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


@pytest.fixture
def other_user() -> User:
    return User(
        id=OTHER_USER_ID,
        name=OTHER_USER_NAME,
        password=OTHER_USER_PASSWORD,
        is_active=OTHER_USER_IS_ACTIVE,
        is_verified=OTHER_USER_IS_VERIFIED,
        created_at=OTHER_USER_CREATED_AT,
        email=OTHER_USER_EMAIL,
        sex=OTHER_USER_SEX,
        birth_date=OTHER_USER_BIRTH_DATE,
        location=OTHER_USER_LOCATION,
        verified_at=OTHER_USER_VERIFIED_AT,
        updated_at=OTHER_USER_UPDATED_AT,
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


@pytest.fixture
def other_profile() -> Profile:
    return Profile(
        user_id=OTHER_USER_ID,
        achievements=OTHER_PROFILE_ACHIEVEMENTS,
        movie_ratings=OTHER_PROFILE_MOVIE_RATINGS,
        series_episode_ratings=OTHER_PROFILE_SERIES_EPISODE_RATINGS,
        approved_reviews=OTHER_PROFILE_APPROVED_REVIEWS,
        movie_reviews=OTHER_PROFILE_MOVIE_REVIEWS,
        series_reviews=OTHER_PROFILE_SERIES_REVIEWS,
        series_season_reviews=OTHER_PROFILE_SERIES_SEASON_REVIEWS,
        series_episode_reviews=OTHER_PROFILE_SERIES_EPISODE_REVIEWS,
        given_votes=OTHER_PROFILE_GIVEN_VOTES,
        gained_votes=OTHER_PROFILE_GAINED_VOTES,
    )


@pytest.fixture(scope="session")
def create_profile() -> CreateProfile:
    return CreateProfile()


@pytest.fixture
def person() -> Person:
    return Person(
        id=PERSON_ID,
        name=PERSON_NAME,
        sex=PERSON_SEX,
        created_at=PERSON_CREATED_AT,
        birth_date=PERSON_BIRTH_DATE,
        birth_place=PERSON_BIRTH_PLACE,
        death_date=PERSON_DEATH_DATE,
        death_place=PERSON_DEATH_PLACE,
        updated_at=PERSON_UPDATED_AT,
    )


@pytest.fixture
def other_person() -> Person:
    return Person(
        id=OTHER_PERSON_ID,
        name=OTHER_PERSON_NAME,
        sex=OTHER_PERSON_SEX,
        created_at=OTHER_PERSON_CREATED_AT,
        birth_date=OTHER_PERSON_BIRTH_DATE,
        birth_place=OTHER_PERSON_BIRTH_PLACE,
        death_date=OTHER_PERSON_DEATH_DATE,
        death_place=OTHER_PERSON_DEATH_PLACE,
        updated_at=OTHER_PERSON_UPDATED_AT,
    )


@pytest.fixture(scope="session")
def create_person() -> CreatePerson:
    return CreatePerson()


@pytest.fixture(scope="session")
def update_person() -> UpdatePerson:
    return UpdatePerson()


@pytest.fixture
def marriage() -> Marriage:
    return Marriage(
        id=MARRIAGE_ID,
        husband_id=MARRIAGE_HUSBAND_ID,
        wife_id=MARRIAGE_WIFE_ID,
        child_ids=MARRIAGE_CHILD_IDS,
        status=MARRIAGE_STATUS,
        start_date=MARRIAGE_START_DATE,
        end_date=MARRIAGE_END_DATE,
    )


@pytest.fixture(scope="session")
def create_marriage() -> CreateMarriage:
    return CreateMarriage()


@pytest.fixture(scope="session")
def update_marriage() -> UpdateMarriage:
    return UpdateMarriage()


@pytest.fixture(scope="session")
def create_relation() -> CreateRelation:
    return CreateRelation()
