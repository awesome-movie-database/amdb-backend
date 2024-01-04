import typer
from alembic import command
from alembic.config import Config


migration_command = typer.Typer(name="migration")


@migration_command.command()
def upgrade() -> None:
    """
    [green]Run[/green] all migrations.
    """
    alembic_config = Config("./amdb/infrastructure/database/alembic.ini")
    command.upgrade(alembic_config, "head")


