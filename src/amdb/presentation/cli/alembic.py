from typing import Annotated

import typer
from alembic import config

from amdb.infrastructure.persistence.alembic.config import ALEMBIC_CONFIG


migration_commands = typer.Typer(name="migration")


@migration_commands.command()
def alembic(commands: Annotated[list[str], typer.Argument()]) -> None:
    """
    [green]Run[/green] alembic.
    """
    config.main(["-c", ALEMBIC_CONFIG, *commands])
