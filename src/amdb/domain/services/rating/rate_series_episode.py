from datetime import datetime
from typing import Optional, Literal, overload

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.user.profile import Profile
from amdb.domain.entities.rating.series_episode_rating import SeriesEpisodeRating
from amdb.domain.value_objects import Rating


class RateSeriesEpisode(Service):
    @overload
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        episode: SeriesEpisode,
        profile: Profile,
        rating: Rating,
        is_counted: Literal[True],
        timestamp: datetime,
    ) -> SeriesEpisodeRating:
        ...

    @overload
    def __call__(
        self,
        *,
        episode: SeriesEpisode,
        profile: Profile,
        rating: Rating,
        is_counted: Literal[False],
        timestamp: datetime,
    ) -> SeriesEpisodeRating:
        ...

    def __call__(
        self,
        *,
        episode: SeriesEpisode,
        profile: Profile,
        rating: Rating,
        is_counted: bool,
        timestamp: datetime,
        series: Optional[Series] = None,
        season: Optional[SeriesSeason] = None,
    ) -> SeriesEpisodeRating:
        profile.series_episode_ratings += 1

        if is_counted:
            self._add_rating_to_series(
                series=series,  # type: ignore[arg-type]
                rating=rating,
            )
            self._add_rating_to_series_season(
                series_season=season,  # type: ignore[arg-type]
                rating=rating,
            )
            self._add_rating_to_series_episode(
                series_episode=episode,
                rating=rating,
            )

        return SeriesEpisodeRating(
            series_id=episode.series_id,
            season_number=episode.season_number,
            episode_number=episode.number,
            user_id=profile.user_id,
            rating=rating,
            is_counted=is_counted,
            created_at=timestamp,
        )

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
