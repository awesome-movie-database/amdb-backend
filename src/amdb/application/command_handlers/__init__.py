__all__ = (
    "RegisterUserHandler",
    "UpdateMyProfileHandler",
    "CreateMovieHandler",
    "DeleteMovieHandler",
    "RateMovieHandler",
    "UnrateMovieHandler",
    "ReviewMovieHandler",
    "AddToWatchlistHandler",
    "DeleteFromWatchlistHandler",
)

from .register_user import RegisterUserHandler
from .update_my_profile import UpdateMyProfileHandler
from .create_movie import CreateMovieHandler
from .delete_movie import DeleteMovieHandler
from .rate_movie import RateMovieHandler
from .unrate_movie import UnrateMovieHandler
from .review_movie import ReviewMovieHandler
from .add_to_watchlist import AddToWatchlistHandler
from .delete_from_watchlist import DeleteFromWatchlistHandler
