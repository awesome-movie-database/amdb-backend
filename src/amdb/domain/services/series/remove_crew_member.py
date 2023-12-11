from datetime import datetime

from amdb.domain.services.base import Service
from amdb.domain.entities.series.series import Series
from amdb.domain.entities.series.season import SeriesSeason
from amdb.domain.entities.series.episode import SeriesEpisode
from amdb.domain.entities.person.person import Person


class RemoveSeriesEpisodeCrewMember(Service):
    def __call__(
        self,
        *,
        series: Series,
        season: SeriesSeason,
        episode: SeriesEpisode,
        crew_member_person: Person,
        timestamp: datetime,
    ) -> None:
        series.updated_at = timestamp
        season.updated_at = timestamp
        episode.updated_at = timestamp
        crew_member_person.updated_at = timestamp
