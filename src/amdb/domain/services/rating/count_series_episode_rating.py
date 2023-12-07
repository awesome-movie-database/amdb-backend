from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.rating.series_episode_rating import SeriesEpisodeRating
from amdb.domain.value_objects import Rating
from amdb.domain.exceptions.rating import SeriesEpisodeRatingAlreadyCountedError


class CountSeriesEpisodeRating(Service):
    def __call__(
        self,
        *,
        episode_rating: SeriesEpisodeRating,
        series: Series,
        season: SeriesSeason,
        episode: SeriesEpisode,
    ) -> None:
        if episode_rating.is_counted:
            raise SeriesEpisodeRatingAlreadyCountedError()

        self._add_rating_to_series(
            series=series,
            rating=episode_rating.rating,
        )
        self._add_rating_to_series_season(
            series_season=season,
            rating=episode_rating.rating,
        )
        self._add_rating_to_series_episode(
            series_episode=episode,
            rating=episode_rating.rating,
        )

        episode_rating.is_counted = True

    def _add_rating_to_series(
        self,
        *,
        series: Series,
        rating: Rating,
    ) -> None:
        series.rating = (series.rating * series.rating_count + rating.value) / (
            series.rating_count + 1
        )
        series.rating_count += 1

    def _add_rating_to_series_season(
        self,
        *,
        series_season: SeriesSeason,
        rating: Rating,
    ) -> None:
        series_season.rating = (
            series_season.rating * series_season.rating_count + rating.value
        ) / (series_season.rating_count + 1)
        series_season.rating_count += 1

    def _add_rating_to_series_episode(
        self,
        *,
        series_episode: SeriesEpisode,
        rating: Rating,
    ) -> None:
        series_episode.rating = (
            series_episode.rating * series_episode.rating_count + rating.value
        ) / (series_episode.rating_count + 1)
        series_episode.rating_count += 1
