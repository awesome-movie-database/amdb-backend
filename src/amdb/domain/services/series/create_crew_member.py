from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.person.person import Person
from amdb.domain.entities.series.crew_member import (
    SeriesEpisodeCrewMember,
    SeriesEpisodeCrewMemberType,
)


class CreateSeriesEpisodeCrewMember(Service):
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        episode: SeriesEpisode,
        person: Person,
        type: SeriesEpisodeCrewMemberType,
        timestamp: datetime,
    ) -> SeriesEpisodeCrewMember:
        series.updated_at = timestamp
        season.updated_at = timestamp
        episode.updated_at = timestamp
        person.updated_at = timestamp

        return SeriesEpisodeCrewMember(
            series_id=series.id,
            season_number=season.number,
            episode_number=episode.number,
            person_id=person.id,
            type=type,
        )
