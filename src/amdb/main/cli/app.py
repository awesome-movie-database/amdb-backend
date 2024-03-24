import os
from typing import Annotated

import typer
from dishka import make_container
from alembic import config

from amdb.infrastructure.persistence.sqlalchemy.config import (
    load_postgres_config_from_toml,
)
from amdb.infrastructure.persistence.redis.config import (
    load_redis_config_from_toml,
)
from amdb.infrastructure.persistence.alembic.config import ALEMBIC_CONFIG
from amdb.presentation.cli.movie import movie_commands
from amdb.main.providers import (
    ConfigsProvider,
    DomainValidatorsProvider,
    DomainServicesProvider,
    ConnectionsProvider,
    EntityMappersProvider,
    ViewModelMappersProvider,
    ApplicationModelMappersProvider,
    SendingAdaptersProvider,
    TaskQueueAdaptersProvider,
    ConvertingAdaptersProvider,
    PasswordManagerProvider,
    ApllicationServicesProvider,
    CommandHandlersProvider,
    CommandHandlerMakersProvider,
    QueryHandlersProvider,
    QueryHandlerMakersProvider,
)
from amdb.main.web_api.app import run_web_api
from amdb.main.worker.app import run_worker


def run_cli() -> None:
    path_to_config = os.getenv("CONFIG_PATH")
    if not path_to_config:
        message = "Path to config env var is not set"
        raise ValueError(message)

    postgres_config = load_postgres_config_from_toml(path_to_config)
    redis_config = load_redis_config_from_toml(path_to_config)

    container = make_container(
        ConfigsProvider(
            postgres_config=postgres_config,
            redis_config=redis_config,
        ),
        DomainValidatorsProvider(),
        ConnectionsProvider(),
        DomainServicesProvider(),
        EntityMappersProvider(),
        ViewModelMappersProvider(),
        ApplicationModelMappersProvider(),
        SendingAdaptersProvider(),
        TaskQueueAdaptersProvider(),
        PasswordManagerProvider(),
        ConvertingAdaptersProvider(),
        ApllicationServicesProvider(),
        CommandHandlersProvider(),
        CommandHandlerMakersProvider(),
        QueryHandlersProvider(),
        QueryHandlerMakersProvider(),
    )

    app = typer.Typer(
        rich_markup_mode="rich",
        context_settings={"obj": {"container": container}},
    )
    app.add_typer(movie_commands)

    @app.command()
    def alembic(commands: Annotated[list[str], typer.Argument()]) -> None:
        """
        [green]Run[/green] alembic.
        """
        config.main(["-c", ALEMBIC_CONFIG, *commands])

    @app.command()
    def web_api() -> None:
        """
        [green]Run[/green] web api.
        """
        run_web_api()

    @app.command()
    def worker() -> None:
        """
        [green]Run[/green] worker.
        """
        run_worker()

    app()
