from dishka import Provider, Scope, provide

from amdb.domain.services import (
    AccessConcern,
    CreateUser,
    UpdateProfile,
    CreateMovie,
    RateMovie,
    UnrateMovie,
    ReviewMovie,
)


class DomainServicesProvider(Provider):
    scope = Scope.APP

    access_concern = provide(AccessConcern, provides=AccessConcern)
    create_user = provide(CreateUser, provides=CreateUser)
    create_movie = provide(CreateMovie, provides=CreateMovie)
    update_profile = provide(UpdateProfile, provides=UpdateProfile)
    rate_movie = provide(RateMovie, provides=RateMovie)
    unrate_movie = provide(UnrateMovie, provides=UnrateMovie)
    review_movie = provide(ReviewMovie, provides=ReviewMovie)
