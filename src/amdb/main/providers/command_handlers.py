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
from amdb.application.common.gateways import (
    UserGateway,
    MovieGateway,
    RatingGateway,
    ReviewGateway,
    PermissionsGateway,
)
from amdb.application.common.unit_of_work import UnitOfWork
from amdb.application.common.password_manager import PasswordManager
from amdb.application.common.identity_provider import (
    IdentityProvider,
)
from amdb.application.command_handlers import (
    RegisterUserHandler,
    UpdateMyProfileHandler,
    CreateMovieHandler,
    DeleteMovieHandler,
    RateMovieHandler,
    UnrateMovieHandler,
    ReviewMovieHandler,
)
from amdb.presentation.create_handler import CreateHandler


class CommandHandlersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register_user(
        self,
        create_user: CreateUser,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        unit_of_work: UnitOfWork,
        password_manager: PasswordManager,
    ) -> RegisterUserHandler:
        return RegisterUserHandler(
            create_user=create_user,
            user_gateway=user_gateway,
            permissions_gateway=permissions_gateway,
            unit_of_work=unit_of_work,
            password_manager=password_manager,
        )

    @provide
    def create_movie(
        self,
        create_movie: CreateMovie,
        movie_gateway: MovieGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateMovieHandler:
        return CreateMovieHandler(
            create_movie=create_movie,
            movie_gateway=movie_gateway,
            unit_of_work=unit_of_work,
        )

    @provide
    def delete_movie(
        self,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
    ) -> DeleteMovieHandler:
        return DeleteMovieHandler(
            movie_gateway=movie_gateway,
            rating_gateway=rating_gateway,
            review_gateway=review_gateway,
            unit_of_work=unit_of_work,
        )


class CommandHandlerMakersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def update_my_profile(
        self,
        update_profile: UpdateProfile,
        user_gateway: UserGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[UpdateMyProfileHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> UpdateMyProfileHandler:
            return UpdateMyProfileHandler(
                update_profile=update_profile,
                user_gateway=user_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def rate_movie_handler(
        self,
        access_concern: AccessConcern,
        rate_movie: RateMovie,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[RateMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> RateMovieHandler:
            return RateMovieHandler(
                access_concern=access_concern,
                rate_movie=rate_movie,
                permissions_gateway=permissions_gateway,
                user_gateway=user_gateway,
                movie_gateway=movie_gateway,
                rating_gateway=rating_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def unrate_movie_handler(
        self,
        access_concern: AccessConcern,
        unrate_movie: UnrateMovie,
        permissions_gateway: PermissionsGateway,
        movie_gateway: MovieGateway,
        rating_gateway: RatingGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[UnrateMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> UnrateMovieHandler:
            return UnrateMovieHandler(
                access_concern=access_concern,
                unrate_movie=unrate_movie,
                permissions_gateway=permissions_gateway,
                movie_gateway=movie_gateway,
                rating_gateway=rating_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def review_movie_handler(
        self,
        access_concern: AccessConcern,
        review_movie: ReviewMovie,
        permissions_gateway: PermissionsGateway,
        user_gateway: UserGateway,
        movie_gateway: MovieGateway,
        review_gateway: ReviewGateway,
        unit_of_work: UnitOfWork,
    ) -> CreateHandler[ReviewMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> ReviewMovieHandler:
            return ReviewMovieHandler(
                access_concern=access_concern,
                review_movie=review_movie,
                permissions_gateway=permissions_gateway,
                user_gateway=user_gateway,
                movie_gateway=movie_gateway,
                review_gateway=review_gateway,
                unit_of_work=unit_of_work,
                identity_provider=identity_provider,
            )

        return create_handler
