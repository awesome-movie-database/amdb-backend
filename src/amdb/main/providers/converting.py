from dishka import Provider, Scope, provide

from amdb.application.common.converting.rating_for_export import (
    RatingsForExportConverter,
)
from amdb.infrastructure.converting.ratings_for_export import (
    RealRatingsForExportConverter,
)


class ConvertingAdaptersProvider(Provider):
    scope = Scope.APP

    ratings_for_export = provide(
        RealRatingsForExportConverter,
        provides=RatingsForExportConverter,
    )
