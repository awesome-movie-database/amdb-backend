from dishka import Provider, Scope, provide

from amdb.domain.services.access_concern import AccessConcern
from amdb.application.common.services import (
    ConvertMyRatingsToFile,
    EnsureCanUseSendingMethod,
)
from amdb.application.common.gateways import (
    UserGateway,
    MovieGateway,
    PermissionsGateway,
)
from amdb.application.common.readers import (
    DetailedMovieViewModelReader,
    DetailedReviewViewModelsReader,
    RatingForExportViewModelsReader,
    NonDetailedMovieViewModelsReader,
    MyDetailedRatingsViewModelReader,
    MyDetailedWatchlistViewModelReader,
)
from amdb.application.common.password_manager import PasswordManager
from amdb.application.common.sending.email import SendEmail
from amdb.application.common.task_queue.export_and_send_my_ratings import (
    EnqueueExportAndSendingMyRatings,
)
from amdb.application.common.identity_provider import (
    IdentityProvider,
)
from amdb.application.query_handlers import (
    LoginHandler,
    GetDetailedMovieHandler,
    GetDetailedReviewsHandler,
    ExportMyRatingsHandler,
    RequestMyRatingsExportHandler,
    ExportAndSendMyRatingsHandler,
    GetMyDetailedRatingsHandler,
    GetNonDetailedMoviesHandler,
    GetMyDetailedWatchlistHandler,
)
from amdb.presentation.create_handler import CreateHandler


class QueryHandlersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def login(
        self,
        access_concern: AccessConcern,
        user_gateway: UserGateway,
        permissions_gateway: PermissionsGateway,
        password_manager: PasswordManager,
    ) -> LoginHandler:
        return LoginHandler(
            access_concern=access_concern,
            user_gateway=user_gateway,
            permissions_gateway=permissions_gateway,
            password_manager=password_manager,
        )

    @provide
    def get_detailed_reviews(
        self,
        movie_gateway: MovieGateway,
        detailed_reviews_reader: DetailedReviewViewModelsReader,
    ) -> GetDetailedReviewsHandler:
        return GetDetailedReviewsHandler(
            movie_gateway=movie_gateway,
            detailed_reviews_reader=detailed_reviews_reader,
        )

    @provide
    def export_and_send_my_ratings(
        self,
        ensure_can_use_sending_method: EnsureCanUseSendingMethod,
        convert_my_ratings_to_file: ConvertMyRatingsToFile,
        user_gateway: UserGateway,
        ratings_for_export_reader: RatingForExportViewModelsReader,
        send_email: SendEmail,
    ) -> ExportAndSendMyRatingsHandler:
        return ExportAndSendMyRatingsHandler(
            ensure_can_use_sending_method=ensure_can_use_sending_method,
            convert_my_ratings_to_file=convert_my_ratings_to_file,
            user_gateway=user_gateway,
            ratings_for_export_reader=ratings_for_export_reader,
            send_email=send_email,
        )


class QueryHandlerMakersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_detailed_movie(
        self,
        detailed_movie_reader: DetailedMovieViewModelReader,
    ) -> CreateHandler[GetDetailedMovieHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetDetailedMovieHandler:
            return GetDetailedMovieHandler(
                detailed_movie_reader=detailed_movie_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_non_detailed_movies(
        self,
        non_detailed_movies_reader: NonDetailedMovieViewModelsReader,
    ) -> CreateHandler[GetNonDetailedMoviesHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetNonDetailedMoviesHandler:
            return GetNonDetailedMoviesHandler(
                non_detailed_movies_reader=non_detailed_movies_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_my_detailed_ratings(
        self,
        my_detailed_ratings_reader: MyDetailedRatingsViewModelReader,
    ) -> CreateHandler[GetMyDetailedRatingsHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetMyDetailedRatingsHandler:
            return GetMyDetailedRatingsHandler(
                my_detailed_ratings_reader=my_detailed_ratings_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def export_my_ratings(
        self,
        convert_my_ratings_to_file: ConvertMyRatingsToFile,
        ratings_for_export_reader: RatingForExportViewModelsReader,
    ) -> CreateHandler[ExportMyRatingsHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> ExportMyRatingsHandler:
            return ExportMyRatingsHandler(
                convert_my_ratings_to_file=convert_my_ratings_to_file,
                ratings_for_export_reader=ratings_for_export_reader,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def request_my_ratings_export(
        self,
        ensure_can_use_sending_method: EnsureCanUseSendingMethod,
        user_gateway: UserGateway,
        enuqueue_export_and_sending: EnqueueExportAndSendingMyRatings,
    ) -> CreateHandler[RequestMyRatingsExportHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> RequestMyRatingsExportHandler:
            return RequestMyRatingsExportHandler(
                ensure_can_use_sending_method=ensure_can_use_sending_method,
                user_gateway=user_gateway,
                enqueue_export_and_sending=enuqueue_export_and_sending,
                identity_provider=identity_provider,
            )

        return create_handler

    @provide
    def get_my_detailed_watchlist(
        self,
        my_detailed_watchlist_reader: MyDetailedWatchlistViewModelReader,
    ) -> CreateHandler[GetMyDetailedWatchlistHandler]:
        def create_handler(
            identity_provider: IdentityProvider,
        ) -> GetMyDetailedWatchlistHandler:
            return GetMyDetailedWatchlistHandler(
                my_detailed_watchlist_reader=my_detailed_watchlist_reader,
                identity_provider=identity_provider,
            )

        return create_handler
