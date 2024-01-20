import importlib.resources

import amdb.infrastructure.persistence.alembic


ALEMBIC_CONFIG = str(
    importlib.resources.files(amdb.infrastructure.persistence.alembic).joinpath("alembic.ini"),
)
