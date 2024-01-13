import typer
import alembic.config
import alembic.command


migration_command = typer.Typer(name="migration")


@migration_command.command()
def run() -> None:
    """
    [green]Run[/green] all migrations.
    """
    alembic_config = alembic.config.Config("./amdb/infrastructure/database/alembic/alembic.ini")
    alembic.command.upgrade(alembic_config, "head")
